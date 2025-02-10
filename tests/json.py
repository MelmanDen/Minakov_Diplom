from utils.json_processor import JsonProcessor
import pytest


@pytest.mark.asyncio
async def test_json_to_dict():
    json_string = '{"key": "value"}'
    data = await JsonProcessor.json_to_dict(json_string=json_string)
    assert isinstance(data, dict)
    assert data == {"key": "value"}


@pytest.mark.asyncio
async def test_dict_to_json():
    data = {"key": "value"}
    json_string = await JsonProcessor.dict_to_json(data=data)
    assert isinstance(json_string, str)
    assert json_string == '{"key": "value"}'
