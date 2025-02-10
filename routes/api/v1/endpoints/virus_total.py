from services.cache.redis_cache import AsyncRedisCache
from utils.factory.header import get_headers_factory
from fastapi import APIRouter, Depends
from services.api.virus_total import VirusTotal
from utils.json_processor import JsonProcessor
from utils.logger_class import Logger
from utils.models.config.virustotal_config import VirusTotalConfig
from utils.models.request.url_payload import URLPayload
from settings import settings
import asyncio

router = APIRouter(
    prefix="/virus_total",
    tags=["virus_total"]
)

redis_cache = AsyncRedisCache(namespace="virus_total")
vt_logger = Logger(name="virus_total")
virus_total = VirusTotal(config=VirusTotalConfig(api_key=settings.virus_total_api_key,
                                                 scan_url=settings.virus_total_scan_url))


@router.post("/get_scan")
async def get_scan_vt(payload: URLPayload,
                      headers: dict = Depends(get_headers_factory(virus_total))):
    if in_cache := await redis_cache.get_value(key=payload.url):
        vt_logger.info(f"Из кэша {in_cache}")
        return await JsonProcessor.json_to_dict(json_string=in_cache)
    vt_logger.info(f"Начало сканирования {payload.url}")
    request_for_scan = await virus_total.get_payload_for_scan(link=payload.url)
    vt_logger.info(f"Запрос для сканирования {request_for_scan}")
    selflink = await virus_total.get_scan_async(data=request_for_scan, headers=headers)
    vt_logger.info(f"Ссылка на сканирование {selflink}")
    for _ in range(settings.checkphish_attempts):
        await asyncio.sleep(settings.checkphish_interval)
        attributes = await virus_total.get_status_async(url=selflink, headers=headers)

        if attributes.get("status") == "completed":
            data = await virus_total.get_meta(attributes=attributes)
            vt_logger.info(f"Результат сканирования {data}")
            await redis_cache.set_value(key=payload.url,
                                        value=await JsonProcessor.dict_to_json(data=data))
            vt_logger.info(f"Запись в кэш {data}")
            return data

    return {"error": "Произошла ошибка при получении статуса сканирования"}
