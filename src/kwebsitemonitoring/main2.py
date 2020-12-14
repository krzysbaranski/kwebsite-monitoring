import json
import logging
import signal
import time
from abc import ABC, abstractmethod
from logging import config as logging_config
from types import FrameType
from typing import List

import confluent_kafka
import psycopg2

from model.message import Message


class InputPipe(ABC):
    @abstractmethod
    def poll(self) -> List[Message]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def is_closed(self) -> bool:
        pass


class OutputPipe(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class KafkaInput(InputPipe):
    def __init__(self, config: dict, topics: str) -> None:
        self.log = logging.getLogger()
        self._consumer = confluent_kafka.Consumer(config)
        self._closed = False
        self._consumer.subscribe(topics.split[","])
        # TODO to config
        self.timeout = 1.0
        self._num_messages = 100

    def poll(self) -> List[Message]:
        # TODO handle errors, extract parser
        messages: List[confluent_kafka.Message] = self._consumer.consume(num_messages=self._num_messages,
                                                                         timeout=self.timeout)
        result: List[Message] = []
        for m in messages:
            j = json.load(m)
            result.append(
                Message(url=j["url"],
                        status=j["status"],
                        response_time_micro=j["response_time_micro"],
                        regexp_checked=j["regexp_checked"],
                        regexp_passed=j["regexp_passed"]
                        )
            )
        return result

    def close(self) -> None:
        self._closed = True
        self._consumer.close()

    def is_closed(self) -> bool:
        return self.closed


class DatabaseOutput(OutputPipe):
    def __init__(self, config: dict, database_table: str) -> None:
        # TODO connection config
        self._conn = psycopg2.connect("dbname=test user=postgres")
        self._cur = self._conn.cursor()
        # TODO db schema
        self._cur.execute(
            "CREATE TABLE IF NOT EXISTS website_check (url varchar, status integer, response_time_micro integer, regexp_checked boolean, regexp_passed boolean);")
        self._flush_interval_ms: int = 10000
        self._flush_timeout = 60.0
        self._last_flush_time_ms: int = int(time.time() * 1000)

    def send(self, message: Message) -> None:
        # TODO handle errors
        self._cur.execute(
            "INSERT INTO website_check(url, status, response_time_micro,regexp_checked,regexp_passed) VALUES (%s, %s, %s, %s, %s)",
            message.url, message.status, message.response_time_micro, message.regexp_checked, message.regexp_passed)
        self._flush()

    def _flush(self) -> None:
        if self._last_flush_time_ms + self._flush_interval_ms < (time.time() * 1000):
            self.log.debug("flush rows")
            self._conn.commit()
            self._last_flush_time_ms = int(time.time() * 1000)

    def close(self) -> None:
        self.log.info("closing database connection")
        self._flush()
        self._cur.close()
        self._conn.close()


class App:
    def __init__(self, config: dict) -> None:
        self.running: bool = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        self._config = config
        self.log = logging.getLogger()

    def main(self) -> None:
        input: InputPipe = KafkaInput(config=self._config["kafka_config"], topic=self._config["kafka_topic"])
        output: OutputPipe = DatabaseOutput(config=self._config["database"], table=self.config["database_table"])

        try:
            while self.running and not input.is_closed():
                websites: List[Message] = input.poll()
                for item in websites:
                    output.send(message=item)
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
