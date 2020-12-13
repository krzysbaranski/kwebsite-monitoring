import logging
import signal
from logging import config as logging_config
from types import FrameType

from kwebsitemonitoring.config import Config


class App:
    def __init__(self, config: Config) -> None:
        self.running: bool = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        self.log = logging.getLogger()

    def main(self):
        while self.running:
            # TODO read from input
            # TODO write result to output
            pass

    def shutdown(self, signal_no: int, stack_frame: FrameType) -> None:
        self.log.warning(f"Shutting down. Received signal: {signal_no} Stack: {stack_frame}")
        self.close()

    def close(self):
        self.running = False


if __name__ == '__main__':
    cfg = Config(logging_config_file="logging.conf")
    logging_config.fileConfig(cfg.logging_config_file)
    App(config=cfg).main()
