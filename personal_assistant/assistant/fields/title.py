from . import Field


class Title(Field):
    MAX_LENGTH = 15

    def is_valid(self, value):
        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                "Title exceeds the maximum length of {} characters.".format(
                    self.MAX_LENGTH))
        return True
