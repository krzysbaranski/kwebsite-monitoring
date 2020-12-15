from abc import abstractmethod, ABC

from typing import List

from model.message import Message

class MessageInput(ABC):
    @abstractmethod
    def poll(self) -> List[Message]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def is_closed(self) -> bool:
        pass
