from . import Field


class Phone(Field):
    def is_valid(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect phone number")
        return True
