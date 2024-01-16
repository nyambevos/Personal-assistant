from . import Field
from datetime import datetime, date


class Date(Field):
    def is_valid(self, value):
        try:
            birthday = datetime.strptime(value, "%Y-%m-%d").date()
            if date.today() < birthday:
                raise ValueError
            return True
        except ValueError:
            raise ValueError("Incorrect date of birth")
