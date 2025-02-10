import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ClientResponseError


class AsyncRequest():
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def post(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        try:
            async with self.session.post(url=url, **kwargs) as response:
                response.raise_for_status()
                if response.status == 200:
                    return await response.json()
        except (ClientConnectorError, ClientResponseError) as e:
            raise e
        finally:
            await self.session.close()

    async def get(self, url: str, headers: dict) -> aiohttp.ClientResponse:
        try:
            async with self.session.get(url=url, headers=headers) as response:
                response.raise_for_status()
                if response.status == 200:
                    return await response.json()
        except (ClientConnectorError, ClientResponseError) as e:
            raise e
        finally:
            await self.session.close()
