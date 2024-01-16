from datetime import datetime
import textwrap
from colored import Fore, Style
from ..fields import Title, Text, Tag, Date


class Note:
    """ This class implements the functionality of a note.
        Accepts values: title, text, tags. """
    def __init__(self, title: str, text: str, tag: str) -> None:
        self._title = Title(title)
        self._text = Text(text)
        self._tags = [Tag(tag)]
        self._creation_date = datetime.now()

    @property
    def title(self) -> Title:
        return self._title

    @title.setter
    def title(self, title) -> None:
        self._title = Title(title)

    @property
    def text(self) -> Text:
        return self._text

    @text.setter
    def text(self, text) -> None:
        self._text = Text(text)

    @property
    def creation_date(self) -> Date:
        return self._creation_date

    @property
    def tags(self) -> set:
        return self._tags

    @property
    def tags_set(self) -> set:
        return set(tag.value for tag in self._tags)

    def add_tag(self, tag: str) -> None:
        """The method adds a new tag to the tag list"""
        tg = self.find_tag(tag=tag)
        if not tg:
            self._tags.append(Tag(tag))
        else:
            raise IndexError(f"{tag} tag already exists.")

    def remove_tag(self, tag: str) -> None:
        """Method removes a tag from the tag list"""
        tg = self.find_tag(tag=tag)

        if tg:
            self._tags.remove(tg)
        else:
            raise IndexError(f"Tag {tag} does not exist")

    def find_tag(self, tag: str) -> Tag:
        """ he method searches for the desired tag.
            If it finds it, it returns it."""
        tg = list(filter(lambda tg: tg.value == tag, self._tags))

        if tg:
            return tg[0]

    def change_tag(self, old_tag: str, new_tag: str):
        """The method replaces the required tag with a new one."""
        tg = self.find_tag(tag=old_tag)

        if tg:
            self._tags.remove(tg)
            self._tags.append(Tag(new_tag))
        else:
            raise IndexError(f"Tag {old_tag} does not exist")

    def __str__(self):
        tags = ', '.join(tuple(tag.value for tag in self.tags))
        tags = textwrap.wrap((tags))
        tags = "\n".join(tuple(f"{line: >70}" for line in tags))
        return f"{Fore.yellow}{str(self.title): <60}{Style.reset}" \
            f"{Fore.dark_gray}" \
            f"{self.creation_date.strftime('%d.%m.%Y')}" \
            f"{Style.reset}\n" \
            f"{'':-^70}\n" \
            f"{textwrap.fill(self.text.value)}\n" \
            f"{Fore.rgb(255, 255, 255)}{tags}{Style.reset}\n"
