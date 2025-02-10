from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api.v1.routes import router
from contextlib import asynccontextmanager
from utils.run_tests import run_tests
from services.cache.redis_cache import AsyncRedisCache
from utils.json_processor import JsonProcessor


@asynccontextmanager
async def lifespan(app: FastAPI):
    vt_client = AsyncRedisCache(namespace="virus_total")
    cp_client = AsyncRedisCache(namespace="checkphish")
    vt_vk_result = {
        "malicious": 0,
        "suspicious": 0,
        "undetected": 26,
        "harmless": 70,
        "timeout": 0
    }
    cp_vk_result = {
        "url": "https://vk.com/im",
        "url_sha256": "02558191bb4b4d58bb7113c22db82725e4b02d1b9f5007a19a0305558fd73f4a",
        "image": "https://bst-prod-screenshots.s3-us-west-2.amazonaws.com/20250115/02558191bb4b4d58bb7113c22db82725e4b02d1b9f5007a19a0305558fd73f4a_1736936531463.png",
        "resolved": False
    }

    vt_yt_result = {
        "malicious": 0,
        "suspicious": 0,
        "undetected": 22,
        "harmless": 68,
        "timeout": 0
    }

    cp_yt_result = {
        "url": "https://translate.yandex.ru/",
        "url_sha256": "c9dbbc47d1e8780575375796058a51e1177269d17c8a81e3df07076dfb14b053",
        "image": "https://bst-prod-screenshots.s3-us-west-2.amazonaws.com/20250115/c9dbbc47d1e8780575375796058a51e1177269d17c8a81e3df07076dfb14b053_1736937743259.png",
        "resolved": False
    }

    vt_gt_result = {
        "malicious": 0,
        "suspicious": 0,
        "undetected": 28,
        "harmless": 68,
        "timeout": 0
    }

    cp_gt_result = {
        "url": "https://translate.google.ru/?sl=auto&tl=ru&op=translate",
        "url_sha256": "67655a532b181abe645006cb40bcbde81ca00967b74c2ff14abff0ee4880d19d",
        "image": "https://bst-prod-screenshots.s3-us-west-2.amazonaws.com/20250115/67655a532b181abe645006cb40bcbde81ca00967b74c2ff14abff0ee4880d19d_1736938356084.png",
        "resolved": False
    }

    expire = 100000
    vk_link = "https://vk.com/im"
    yt_link = "https://translate.yandex.ru/"
    gt_link = "https://translate.google.ru/?sl=auto&tl=ru&op=translate"
    await vt_client.set_value(key=vk_link, value=await JsonProcessor.dict_to_json(data=vt_vk_result), expire=expire)
    await cp_client.set_value(key=vk_link, value=await JsonProcessor.dict_to_json(data=cp_vk_result), expire=expire)

    await vt_client.set_value(key=yt_link, value=await JsonProcessor.dict_to_json(data=vt_yt_result), expire=expire)
    await cp_client.set_value(key=yt_link, value=await JsonProcessor.dict_to_json(data=cp_yt_result), expire=expire)

    await vt_client.set_value(key=gt_link, value=await JsonProcessor.dict_to_json(data=vt_gt_result), expire=expire)
    await cp_client.set_value(key=gt_link, value=await JsonProcessor.dict_to_json(data=cp_gt_result), expire=expire)

    await run_tests()
    yield


app = FastAPI(title="URL Scanner API", version="1.0.0", lifespan=lifespan)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
