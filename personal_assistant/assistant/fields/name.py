from . import Field


class Name(Field):
    def is_valid(self, value: str):
        if value.isalpha():
            return True
        raise ValueError('Incorrect name format')
