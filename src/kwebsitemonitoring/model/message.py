from dataclasses import dataclass


@dataclass
class Message:
    url: str
    status: int
    response_time_micro: float
    regexp_checked: bool
    regexp_passed: bool
