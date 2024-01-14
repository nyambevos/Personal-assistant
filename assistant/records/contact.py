""" Модуль роботи з контактом """

from assistant.fields import Address, Date
from assistant.fields import EmailAddress, Name, Phone


class Contact:
    def __init__(self, name: str):
        self._name = Name(name)
        self._phones = []
        self._address = None
        self._email = None
        self._birthday = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = Name(name)

    @property
    def phones(self):
        return self._phones

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = Address(address)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = EmailAddress(email)

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        self._birthday = Date(birthday)

    def add_phone(self, new_phone):
        for phone in self._phones:
            if phone.value == new_phone:
                raise IndexError(f"Phone {new_phone} is already in phone numbers list")
        self._phones.append(Phone(new_phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self._phones:
            if new_phone == phone.value:
                raise IndexError(f"Phone {new_phone} is already in phone numbers list")
            elif old_phone == phone.value:
                self._phones[self._phones.index(phone)] = Phone(new_phone)
                break
            else:
                raise IndexError(f"There is no such phone {old_phone} in phone numbers list")

    def remove_phone(self, old_phone):
        for phone in self._phones:
            if phone.value == old_phone:
                self._phones.remove(phone)
                break
        else:
            raise IndexError(f"There is no such phone {old_phone} in phone numbers list")