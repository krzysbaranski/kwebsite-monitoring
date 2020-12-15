from abc import abstractmethod, ABC

from model.message import Message


class MessageOutput(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

