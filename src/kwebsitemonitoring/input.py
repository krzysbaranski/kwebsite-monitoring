from abc import abstractmethod

from typing import List

from src.kwebsitemonitoring.website import Website


class Input:
    @abstractmethod
    def poll(self) -> List[Website]:
        pass