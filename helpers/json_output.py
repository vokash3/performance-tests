import json


class JSONOutput:
    def get_json(self, raw_json) -> str:
        return json.dumps(raw_json, sort_keys=True, indent=4, ensure_ascii=False)
