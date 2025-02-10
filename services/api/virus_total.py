from typing import Any, Dict
from utils.abstract.scanner import ScanManager
from services.network.async_net import AsyncRequest
from utils.models.config.virustotal_config import VirusTotalConfig
from utils.models.response.summary import Summary


class VirusTotal(ScanManager):
    def __init__(self, config: VirusTotalConfig):
        self.api_key = config.api_key
        self.scan_url = config.scan_url
        self.accept = config.accept

    async def get_payload_for_scan(self, link: str) -> Dict[str, str]:
        return {"url": link}

    async def get_headers(self) -> Dict[str, str]:
        return {
            "accept": self.accept,
            "x-apikey": self.api_key
        }

    async def get_scan_async(self, **kwargs) -> Dict[str, Any]:
        response: dict = await AsyncRequest().post(self.scan_url, **kwargs)
        return response.get("data").get("links").get("self")

    async def get_status_async(self, url: str, **kwargs) -> Dict[str, Any]:
        response = await AsyncRequest().get(url, **kwargs)
        return response.get("data").get("attributes")

    @staticmethod
    async def get_meta(attributes: Dict[str, any]) -> Summary:
        return attributes.get("stats")
