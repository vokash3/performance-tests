import json

from pydantic import BaseModel


class JSONOutput:
    @staticmethod
    def get_json(data) -> str:
        """
        Get nice json string (dumped) from data
        :param data: str | dict | BaseModel
        :return: Красивый json string
        """
        if isinstance(data, BaseModel):
            return data.model_dump_json(indent=4, ensure_ascii=False)
        return json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
