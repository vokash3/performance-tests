import json

from pydantic import BaseModel


class JSONOutput:
    @staticmethod
    def get_json(raw_json) -> str:
        """
        Get nice json string (dumped) from raw_json
        :param raw_json:
        :return: Красивый json string
        """
        if isinstance(raw_json, BaseModel):
            return raw_json.model_dump_json(indent=4, ensure_ascii=False)
        return json.dumps(raw_json, sort_keys=True, indent=4, ensure_ascii=False)
