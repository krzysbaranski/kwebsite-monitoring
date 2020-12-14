from abc import abstractmethod, ABC

from typing import List

from model.website import Website


class Input(ABC):
    @abstractmethod
    def poll(self) -> List[Website]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass