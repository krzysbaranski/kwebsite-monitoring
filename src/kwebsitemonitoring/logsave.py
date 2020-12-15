import json
import logging
import signal
from logging import config as logging_config
from types import FrameType
from typing import List

import confluent_kafka

from input.messageinput import MessageInput
from model.message import Message
from output.databaseoutput import DatabaseOutput
from output.messageoutput import MessageOutput


class KafkaInput(MessageInput):
    def __init__(self, config: dict, topics: str) -> None:
        self.log = logging.getLogger()
        self._consumer = confluent_kafka.Consumer(config)
        self._closed = False
        self._consumer.subscribe(topics=topics.split(","))
        # TODO to config
        self.timeout = 1.0
        self._num_messages = 100

    def poll(self) -> List[Message]:
        # TODO handle errors, extract parser
        messages: List[confluent_kafka.Message] = self._consumer.consume(num_messages=self._num_messages,
                                                                         timeout=self.timeout)
        result: List[Message] = []
        for m in messages:
            j = json.loads(m.value())
            result.append(
                self._parse_message(j)
            )
        return result

    def _parse_message(self, message: confluent_kafka.Message):
        return Message(url=message["url"],
                       status=message["status"],
                       response_time_micro=message["response_time_micro"],
                       regexp_checked=message["regexp_checked"],
                       regexp_passed=message["regexp_passed"]
                       )

    def close(self) -> None:
        self._closed = True
        self._consumer.close()

    def is_closed(self) -> bool:
        return self._closed





class App:
    def __init__(self, config: dict) -> None:
        self.running: bool = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        self._config = config
        self.log = logging.getLogger()

    def main(self) -> int:
        input: MessageInput = KafkaInput(config=self._config["kafka_config"], topics=self._config["kafka_topic"])
        output: MessageOutput = DatabaseOutput(config=self._config["database"], table=self._config["database_table"])

        try:
            while self.running and not input.is_closed():
                websites: List[Message] = input.poll()
                for item in websites:
                    output.send(message=item)
        except Exception as e:
            self.log.exception(f"Exception in main loop: {e}")
            raise e
        finally:
            if input:
                input.close()
            if output:
                output.close()

    def shutdown(self, signal_no: int, stack_frame: FrameType) -> None:
        self.log.warning(f"Shutting down. Received signal: {signal_no} Stack: {stack_frame}")
        self.close()

    def close(self) -> None:
        self.running = False


if __name__ == '__main__':
    # TODO better and safe config support (no dict)
    with open("config.json") as f:
        config = json.load(f)

    logging_config.fileConfig(config["logging_config_file"])
    App(config=config).main()
