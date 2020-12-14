import json
import logging
import time

from confluent_kafka import Producer, KafkaException
from dataclasses import asdict

from model.message import Message
from output.output import Output


class KafkaOutput(Output):
    def __init__(self, config: dict, topic: str):
        self.log = logging.getLogger()
        self._config = config
        self._topic = topic
        self._producer: Producer = self._connect()
        # TODO move to config
        self._flush_interval_ms: int = 10000
        self._flush_timeout = 60.0
        self._last_flush_time_ms: int = int(time.time() * 1000)

    def _connect(self) -> Producer:
        return Producer(self._config)

    def send(self, message: Message):
        """
        async send, without guarantee to be delivered
        """
        self._flush()
        payload: str = self._convert(message)
        self.log.debug(f"producing message {payload}")
        self._producer.produce(topic=self._topic, value=payload)

    def _flush(self):
        if self._last_flush_time_ms + self._flush_interval_ms < (time.time() * 1000):
            self.log.debug("flush producer")
            self._producer.flush(self._flush_timeout)
            self._last_flush_time_ms = int(time.time() * 1000)

    def _convert(self, message: Message) -> str:
        return json.dumps(asdict(message))

    def close(self) -> None:
        self.log.info("Closing kafka producer")
        self._producer.flush()
