from typing import Callable


def get_headers_factory(object: Callable) -> Callable:
    async def get_headers() -> dict:
        return await object.get_headers()
    return get_headers
