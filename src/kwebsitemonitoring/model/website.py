from typing import Union

from dataclasses import dataclass


@dataclass
class Website:
    url: str
    regexp: Union[str, None]
