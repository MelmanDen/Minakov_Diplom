from utils.factory.header import get_headers_factory
from fastapi import APIRouter, Depends
from services.api.checkphish import CheckPhish
from utils.models.config.checkphish_config import CheckPhishConfig
from utils.models.request.url_payload import URLPayload
from utils.logger_class import Logger
from settings import settings
import asyncio
from services.cache.redis_cache import AsyncRedisCache
from utils.json_processor import JsonProcessor

router = APIRouter(
    prefix="/checkphish",
    tags=["checkphish"]
)

redis_cache = AsyncRedisCache(namespace="checkphish")
cp_logger = Logger(name="checkphish")
checkphish = CheckPhish(config=CheckPhishConfig(api_key=settings.checkphish_api_key,
                                                scan_url=settings.checkphish_scan_url,
                                                status_url=settings.checkphish_status_url))


@router.post("/get_scan")
async def get_scan_cp(payload: URLPayload,
                      headers: dict = Depends(get_headers_factory(checkphish))):
    if in_cache := await redis_cache.get_value(key=payload.url):
        cp_logger.info(f"Из кэша {in_cache}")
        return await JsonProcessor.json_to_dict(json_string=in_cache)

    cp_logger.info(f"Начало сканирования {payload.url}")
    request_for_scan = await checkphish.get_payload_for_scan(link=payload.url)
    job_id = await checkphish.get_scan_async(json=request_for_scan, headers=headers)

    for _ in range(settings.virus_total_attempts):
        await asyncio.sleep(settings.virus_total_interval)
        request_for_status = await checkphish.get_payload_for_status(job_id=job_id)
        response = await checkphish.get_status_async(json=request_for_status, headers=headers)

        if response.get("status") == "DONE":
            result = await checkphish.get_meta(response=response)
            cp_logger.info(f"Результат сканирования {result}")
            data = result.model_dump()
            await redis_cache.set_value(key=payload.url,
                                        value=await JsonProcessor.dict_to_json(data=data))
            cp_logger.info(f"Запись в кэш {data}")
            return result

    return {"error": "Произошла ошибка при получении статуса сканирования"}
