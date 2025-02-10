from utils.abstract.scanner import ScanManager
from services.network.async_net import AsyncRequest
from typing import Any, Dict
from utils.models.config.checkphish_config import CheckPhishConfig
from utils.models.response.meta import Meta


class CheckPhish(ScanManager):
    def __init__(self, config: CheckPhishConfig):
        self.api_key = config.api_key
        self.scan_url = config.scan_url
        self.status_url = config.status_url

    async def get_payload_for_scan(self, link: str) -> Dict[str, str]:
        return {
            "apiKey": self.api_key,
            "urlInfo": {
                "url": link
            }
        }

    async def get_payload_for_status(self, job_id: str) -> Dict[str, str]:
        return {
            "apiKey": self.api_key,
            "jobID": job_id,
            "insights": True
        }

    @staticmethod
    async def get_headers() -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    async def get_scan_async(self, **kwargs) -> str:
        response: dict = await AsyncRequest().post(self.scan_url, **kwargs)
        return response.get("jobID")

    async def get_status_async(self, **kwargs) -> Dict[str, Any]:
        return await AsyncRequest().post(self.status_url, **kwargs)

    @staticmethod
    async def get_meta(response: Dict[str, any]) -> Meta:
        meta = Meta(
            url=response.get("url"),
            url_sha256=response.get("url_sha256"),
            image=response.get("screenshot_path"),
            resolved=response.get("resolved")
        )
        return meta
