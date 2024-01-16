import re
from . import Field


class EmailAddress(Field):
    def is_valid(self, value):
        if re.search(
            r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$",
            value
        ):
            return True
        raise ValueError("Incorrect e-mail format")
