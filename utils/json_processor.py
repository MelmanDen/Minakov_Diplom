import json


class JsonProcessor:
    @staticmethod
    async def json_to_dict(json_string: str) -> dict:
        return json.loads(json_string)

    @staticmethod
    async def dict_to_json(data: dict) -> str:
        return json.dumps(data)
