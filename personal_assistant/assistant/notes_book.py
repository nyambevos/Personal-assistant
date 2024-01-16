from collections import UserList
from .records import Note


class NoteBook(UserList):
    """ The class for working with the contact book,
        inherited from the UserList class."""
    def add_record(self, record: Note) -> None:
        """ A method for adding entries to a contact book.
            Accepts one parameter of type Note."""
        self.data.append(record)

    def find(self, keyword: str, tag_only: bool = False) -> list:
        match_records = []

        for record in self.data:
            """ The method performs a global search by
                Title, Text, Tag values.
                Accepts one required keyword argument of type str,
                and one optional tag_only argument of type bool.
                By default, tag_only is False. If tag_only is True,
                the search will be performed only by tags."""
            if not tag_only:
                if (keyword in record.title.value or
                        keyword in record.text.value):
                    match_records.append(record)
                    continue

            for tag in record.tags:
                if keyword in tag.value:
                    match_records.append(record)
                    break

        return match_records if match_records else None

    def delete(self, title):
        """ The method deletes an entry from the notebook by title.
            Accepts one argument title of type str"""
        note = self.get_note(title)
        self.data.remove(note)

    def get_note(self, title: str) -> Note:
        """ The method returns a record by its title.
            If such a record does not exist,
            an IndexError exception is thrown.
            Accepts one argument title of type str."""
        for record in self.data:
            if title == record.title.value:
                return record

        raise IndexError("Such a contact does not exist")

    def iterator(self, amount=1):
        """ The iterator method. Accepts one optional argument
            amount of type int. amount defaults to 1.
            amount determines the number of objects that
            the method will return in one iteration."""
        index = 0
        while index < len(self.data):
            yield self.data[index:index + amount]
            index += amount

    @property
    def notes_tags_set(self):
        tags = set()
        for note in self.data:
            tags.update(note.tags_set)
        return tags

    @property
    def titles_tuple(self):
        return tuple(note.title.value for note in self.data)
