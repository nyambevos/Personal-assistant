class Field:
    """ This class accepts the value value, checks
      it using the is_value method, and if the value
      passes the check, the value is written to the
      _value class field. """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self._value = value

    def is_valid(self, value):
        """ This method performs a value check, and
        if the check is successful, returns True, and
        if not, throws an exception of type ValueError """
        return True
