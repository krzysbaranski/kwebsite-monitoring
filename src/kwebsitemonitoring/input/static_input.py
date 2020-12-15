from typing import List

from input.websiteinput import WebsiteInput
from model.website import Website


class StaticInput(WebsiteInput):
    def __init__(self, config: dict):
        self._data: List[Website] = []
        self._closed = False
        for item in config:
            self._data.append(Website(url=item["url"], regexp=item["regexp"]))

    def poll(self) -> List[Website]:
        return self._data

    def close(self):
        self._closed = True

    def is_closed(self):
        return self._closed
