""" Модуль роботи з контактом """

from assistant.fields import Address, Date
from assistant.fields import EmailAddress, Name, Phone


class Contact:

    def __init__(self, name:str):
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

    def add_phone(self, phone):
        if phone in self._phones:
            raise IndexError(f"Phone {phone} is already in phone numbers list")
        else:
            self._phones.append(Phone(phone))

    def edit_phone(self, phone, new_phone):
        if new_phone in self._phones:
            raise IndexError(f"Phone {new_phone} is already in phone numbers list")
        elif phone in self._phones:
            self._phones[self._phones.index(phone)] = new_phone
        else:
            raise IndexError(f"There is no such phone {phone} in phone numbers list")

    def remove_phone(self, phone):
        if phone in self._phones:
            self._phones.remove(phone)
        else:
            raise IndexError(f"There is no such phone {phone} in phone numbers list")