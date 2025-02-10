import pytest
from aioresponses import aioresponses
from services.network.async_net import AsyncRequest
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_post_success():
    url = 'https://httpbin.org/post'
    response_data = {'json': {'key': 'value'}}

    with aioresponses() as m:
        m.post(url, payload=response_data)
        response = await AsyncRequest().post(url, json={'key': 'value'})
        assert response == response_data


@pytest.mark.asyncio
async def test_get_success():
    url = 'https://httpbin.org/get'
    headers = {'Authorization': 'Bearer token'}
    response_data = {'headers': headers}

    with aioresponses() as m:
        m.get(url, payload=response_data)
        response = await AsyncRequest().get(url, headers=headers)
        assert response == response_data
