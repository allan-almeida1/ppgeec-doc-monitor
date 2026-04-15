import json
import os
from typing import List

from schemas import News


class DataHandler:
    def __init__(self):
        self.filepath = "data/last_scan.json"
        self.data = self._load_data()

    def _load_data(self) -> List[News]:
        try:
            if not os.path.exists(self.filepath):
                return []

            if os.path.getsize(self.filepath) == 0:
                return []

            with open(self.filepath, "r") as f:
                data = json.load(f)
                return [News(**item) for item in data]

        except json.JSONDecodeError:
            return []

    def save_data(self, data: List[News]):
        with open(self.filepath, "w") as f:
            json.dump(
                [item.model_dump(mode="json") for item in data],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def get_data(self) -> List[News]:
        return self.data


__all__ = ["DataHandler"]
