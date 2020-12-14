from typing import List

from input.input import Input
from model.website import Website


class StaticInput(Input):
    def __init__(self, config: dict):
        self._data: List[Website] = []
        for item in config:
            self._data.append(Website(url=item["url"], regexp=item["regexp"]))

    def poll(self) -> List[Website]:
        return self._data

    def close(self):
        pass
