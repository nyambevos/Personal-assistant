from collections import UserList
from datetime import date, datetime, timedelta


class ContactBook(UserList):
    def add_contact(self, new_contact):
        for contact in self.data:
            if contact.name.value == new_contact.name.value:
                raise ValueError(
                    f"Contact with name {new_contact.name}"
                    " is already in Contact Book"
                )
        self.data.append(new_contact)

    def edit_name(self, name, new_name):
        for contact in self.data:
            if contact.name.value == name:
                contact.name = new_name
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def edit_phone(self, name, old_phone, new_phone):
        for contact in self.data:
            if contact.name.value == name:
                contact.edit_phone(old_phone, new_phone)
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def edit_address(self, name, address):
        for contact in self.data:
            if contact.name.value == name:
                contact.address = address
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def edit_email(self, name, email):
        for contact in self.data:
            if contact.name.value == name:
                contact.address = email
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def edit_birthday(self, name, birthday):
        for contact in self.data:
            if contact.name.value == name:
                contact.birthday = birthday
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def delete_contact(self, name):
        for contact in self.data:
            if contact.name.value == name:
                self.data.remove(contact)
                break
        else:
            raise IndexError(f'Contact with name {name} not found')

    def get_contact(self, name):
        for contact in self.data:
            if contact.name.value == name:
                return contact
        else:
            raise IndexError(f'Contact with name {name} not found')

    def find(self, key_word):
        matching_contacts = []

        for contact in self.data:
            if (contact.name.value and key_word
                in contact.name.value) or (
                    contact.address and key_word
                    in contact.address.value) or (
                    contact.email and key_word
                    in contact.email.value) or (
                    contact.birthday and key_word
                    in contact.birthday.value) or any(
                    phone.value and key_word
                    in phone.value for phone
                    in contact.phones):
                matching_contacts.append(contact)

        return matching_contacts

    def days_to_birthday(self, days):
        today = date.today()
        target_date = today + timedelta(days=days)

        upcoming_birthday_contacts = []

        for contact in self.data:
            if contact.birthday is not None:
                birthday = datetime.strptime(
                    contact.birthday.value, "%Y-%m-%d"
                )
                next_birthday = datetime(
                    today.year, birthday.month, birthday.day
                ).date()
                if today > next_birthday:
                    next_birthday = datetime(
                        today.year + 1, birthday.month, birthday.day
                    ).date()

                if next_birthday == target_date:
                    upcoming_birthday_contacts.append(contact)

        return upcoming_birthday_contacts

    @property
    def names_tuple(self):
        return tuple(contact.name.value for contact in self.data)
