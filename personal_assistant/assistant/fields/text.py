from . import Field


class Text(Field):
    MAX_LENGTH = 250

    def is_valid(self, value):
        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                "Text exceeds the maximum length of {} characters.".format(
                    self.MAX_LENGTH))
        return True
