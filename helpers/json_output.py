import json


class JSONOutput:
    @staticmethod
    def get_json(raw_json) -> str:
        """
        Get nice json string (dumped) from raw_json
        :param raw_json:
        :return: Красивый json string
        """
        return json.dumps(raw_json, sort_keys=True, indent=4, ensure_ascii=False)
