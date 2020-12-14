import re


class RegexpCheck:
    def __init__(self):
        pass

    def check(self, regexp: str, content: str) -> bool:
        if not content:
            return False
        re_compiled = re.compile(".*"+regexp+".*")
        for line in content.splitlines():
            match = re_compiled.match(line)
            if match:
                return True
        return False
