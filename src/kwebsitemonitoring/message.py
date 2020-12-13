from dataclasses import dataclass

from typing import Union


@dataclass
class Message:
    url: str
    status: int
    regexp_checked: bool
    regexp_passed: Union[bool, None]