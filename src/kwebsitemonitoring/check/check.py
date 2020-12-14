from abc import abstractmethod

from model.message import Message
from model.website import Website


class Check:
    def __init__(self):
        pass

    @abstractmethod
    def check(self, website: Website) -> Message:
        pass
