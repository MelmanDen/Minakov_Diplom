from abc import ABC, abstractmethod


class ScanManager(ABC):

    @abstractmethod
    async def get_payload_for_scan(self, **kwargs):
        pass

    @abstractmethod
    async def get_headers(self, **kwargs):
        pass

    @abstractmethod
    async def get_scan_async(self, **kwargs):
        pass

    @abstractmethod
    async def get_status_async(self, **kwargs):
        pass

    @abstractmethod
    async def get_meta(self, **kwargs):
        pass
