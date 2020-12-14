from abc import abstractmethod, ABC

from model.message import Message


class Output(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
