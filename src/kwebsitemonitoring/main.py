import json
import logging
import signal
from logging import config as logging_config
from types import FrameType

from check.check import Check
from check.request_check import RequestCheck
from input.input import Input
from input.static_input import StaticInput
from model.message import Message
from output.kafka import KafkaOutput
from output.output import Output


class App:
    def __init__(self, config: dict) -> None:
        self.running: bool = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        self._config = config
        self.log = logging.getLogger()

    def main(self) -> None:
        input: Input = StaticInput(config=self._config["websites"])
        output: Output = KafkaOutput(config=self._config["kafka_config"], topic=self._config["kafka_topic"])
        check: Check = RequestCheck()
        try:
            while self.running:
                websites = input.poll()
                # TODO configure min time between consecutive checks
                # TODO parallel checks
                for item in websites:
                    message: Message = check.check(website=item)
                    output.send(message=message)
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
