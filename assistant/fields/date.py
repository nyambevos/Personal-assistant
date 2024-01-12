""" Модуль поля дати дня народження """

from assistant.fields import Field

class Date(Field):
    def is_valid(self, value):
        try:
            birthday = datetime.strptime(value, "%Y-%m-%d").date()
            if date.today() < birthday:
                return False
            return True
        except ValueError:
            return False