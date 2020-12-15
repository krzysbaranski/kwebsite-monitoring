import logging
import time

import psycopg2

from model.message import Message
from output.messageoutput import MessageOutput


class DatabaseOutput(MessageOutput):
    def __init__(self, config: dict, table: str) -> None:
        # TODO connection config
        self.log = logging.getLogger()
        self._table = table
        self._conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"])
        self._cur = self._conn.cursor()
        # TODO db schema
        self._cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self._table} (url varchar, status integer, response_time_micro integer, regexp_checked boolean, regexp_passed boolean);")
        self._flush_interval_ms: int = 10000
        self._flush_timeout = 60.0
        self._last_flush_time_ms: int = int(time.time() * 1000)

    def send(self, message: Message) -> None:
        # TODO handle errors
        self._cur.execute(
            f"INSERT INTO {self._table} (url, status, response_time_micro,regexp_checked,regexp_passed) VALUES (%s, %s, %s, %s, %s)",
            (message.url, message.status, message.response_time_micro, message.regexp_checked, message.regexp_passed))
        self.log.debug(f"saved row {message} to table {self._table}")
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