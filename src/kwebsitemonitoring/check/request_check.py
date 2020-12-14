import requests
from requests import RequestException

from check.check import Check
from check.regexp_check import RegexpCheck
from model.message import Message
from model.website import Website


class RequestCheck(Check):
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.regex_check: RegexpCheck = RegexpCheck()

    def check(self, website: Website) -> Message:
        # TODO support headers (auth, content-type etc);
        try:
            r = requests.get(url=website.url, timeout=self.timeout)
            regexp_check_passed: bool = False
            regexp_checked: bool = False
            if website.regexp:
                regexp_check_passed = self.regex_check.check(
                    regexp=website.regexp,
                    content=r.text)
                regexp_checked = True

            return Message(url=website.url,
                           status=r.status_code,
                           response_time_micro=r.elapsed.microseconds,
                           regexp_checked=regexp_checked,
                           regexp_passed=regexp_check_passed)

        except (RequestException, Exception) as e:
            return Message(url=website.url,
                           status=None,
                           response_time_micro=None,
                           regexp_checked=False,
                           regexp_passed=False)
