from pathlib import Path
from pickle import UnpicklingError
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colored import Fore, Style
from .fields import Address, Date, EmailAddress
from .fields import Name, Phone, Tag, Text, Title
from .records import Contact, Note
from .notes_book import NoteBook
from .contact_book import ContactBook
from .utils.data_handler import save_data_to_file
from .utils.data_handler import load_data_from_file
from .file_sorter import init_folder


commands = {}


# command handler decorator to handle commands automaticaly
# usage: @command_handler(command, description)
#        def method(self)
#
# as result dict commands
# commands = {
#    command_name1: (method1, description1)
#    command_name2: (method2, description2)
# }
# to call method inside class: commands[command_name][0]
# to get description: command[command_name][1]
#
# to add new method to class just simply apply decorator
# command will be added to dict automatically
def command_handler(command, description):
    def input_error(func):
        def wrapper(self):
            try:
                return func(self)
            except (ValueError, IndexError, FileNotFoundError) as err:
                return f"{Fore.red}{err}{Style.reset}"
        commands[command] = (wrapper, description)
        return wrapper
    return input_error


class Assistant:
    def __init__(self) -> None:
        self.running = True
        self.contact_book = ContactBook()
        self.notes_book = NoteBook()

    @staticmethod
    def validated_input(
        verify_cls,
        request,
        completer=None,
        allow_empty=False
    ):
        inp_completer = WordCompleter(completer) if completer else None
        while True:
            try:
                inp = prompt(request, completer=inp_completer).strip()
                if not inp and allow_empty:
                    return None
                if not inp:
                    raise ValueError("Input can't be empty")
                return verify_cls(inp)
            except (ValueError, IndexError) as err:
                print(f"{Fore.red}{err}{Style.reset}")

    def save(self):
        dir_path = Path.home().joinpath(".personal_assistant")
        if not dir_path.exists():
            dir_path.mkdir()
        save_data_to_file(
            dir_path.joinpath("contact_book.bin"),
            self.contact_book
        )
        save_data_to_file(
            dir_path.joinpath("notes_book.bin"),
            self.notes_book
        )

    def load(self):
        dir_path = Path.home().joinpath(".personal_assistant")
        try:
            self.contact_book = load_data_from_file(
                dir_path.joinpath("contact_book.bin")
            )
        except (UnpicklingError, FileNotFoundError, ModuleNotFoundError):
            pass
        try:
            self.notes_book = load_data_from_file(
                dir_path.joinpath("notes_book.bin")
            )
        except (UnpicklingError, FileNotFoundError, ModuleNotFoundError):
            pass

    @command_handler("help", "Help")
    def help(self):
        return "Usage: type a command "\
            "or press TAB to command menu\n"\
            "list - list all commands"

    @command_handler("list", "List all commands")
    def list_command(self):
        return "\n".join(
            f"{command: <17}{val[1]}" for command, val in commands.items()
        )

    @command_handler("about", "About this application")
    def about(self):
        return f"\n{Fore.rgb(255, 255, 255)}This console program "\
            "is a fast and easy to use personal assisstant to store"\
            f"your contacts and notes.{Style.reset}\n\n"\
            f"{Fore.yellow}Contributors:{Style.reset}\n"\
            "Ruslan Bilokoniuk aka Nyambevos - Team Lead\n"\
            "Andrii Trebukh - Scrum Master\n"\
            "Олена Сазонець\n"\
            "Olha Lialina\n"\
            "Eugene Vlasenko\n"

    @command_handler("exit", "Exit")
    def exit_command(self):
        self.running = False
        return "Bye!"

    @command_handler("add", "Add new user to contact book")
    def add_command(self):
        name = self.validated_input(Name, "User name: ")
        contact = Contact(name.value)
        self.contact_book.add_contact(contact)
        phone = self.validated_input(
            Phone,
            "User phone in 10 digits format, empty to skip: ",
            allow_empty=True)
        if phone:
            contact.add_phone(phone.value)
        address = self.validated_input(
            Address,
            "User address, empty to skip: ",
            allow_empty=True
        )
        if address:
            contact.address = address.value
        email = self.validated_input(
            EmailAddress,
            "User e-mail, empty to skip: ",
            allow_empty=True
        )
        if email:
            contact.email = email.value
        birthday = self.validated_input(
            Date,
            "User birthday in YYYY-MM-DD format, empty to skip: ",
            allow_empty=True
        )
        if birthday:
            contact.birthday = birthday.value
        return f"New user has been added:\n\n{contact}"

    @command_handler("remove", "Remove user from contact book")
    def remove_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        self.contact_book.delete_contact(name.value)
        return f"User {name.value} has been removed"

    @command_handler("phone add", "Add phone number to existing user")
    def add_phone_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        phone = self.validated_input(
            Phone,
            "User phone in 10 digits format: "
        )
        contact.add_phone(phone.value)
        return f"Phone {phone.value} has been added"

    @command_handler("phone remove", "Femove phone number from existing user")
    def rm_phone_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        phone = self.validated_input(
            Phone,
            "User phone, empty to skip: ",
            contact.phones_tuple,
            allow_empty=True
        )
        if phone is None:
            return "Nothing has been removed"
        contact.remove_phone(phone.value)
        return f"Phone {phone.value} has been removed"

    @command_handler("phone edit", "Edit existing phone number")
    def edit_phone_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        phone = self.validated_input(
            Phone,
            "User phone, empty to skip: ",
            contact.phones_tuple,
            allow_empty=True
        )
        if phone is None:
            return "Nothing has been changed"
        new_phone = self.validated_input(
            Phone,
            "New phone in 10 digits format: "
        )
        contact.edit_phone(phone.value, new_phone.value)
        return f"Phone {phone.value} has been changed to {new_phone.value}"

    @command_handler("edit name", "Edit existing user name")
    def edit_name_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        new_name = self.validated_input(
            Name,
            "New user name, empty to skip: ",
            allow_empty=True
        )
        if new_name is None:
            return "Nothing has been changed"
        contact.name = new_name.value
        return f"User name {name.value} has been changed to {new_name.value}"

    @command_handler("address", "Add or overwrite existing user address")
    def edit_address_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        address = self.validated_input(
            Address,
            "User address, empty to skip: ",
            allow_empty=True
        )
        if address is None:
            return "Nothing has been changed"
        contact.address = address.value
        return f"User address has been changed to {address.value}"

    @command_handler("e-mail", "Add or overwrite existing user e-mail")
    def edit_email_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        email = self.validated_input(
            EmailAddress,
            "User e-mail, empty to skip: ",
            allow_empty=True
        )
        if email is None:
            return "Nothing has been changed"
        contact.email = email.value
        return f"User email has been changed to {email.value}"

    @command_handler("birthday", "Add or overwrite existing user birthday")
    def edit_birthday_command(self):
        name = self.validated_input(
            Name,
            "User name: ",
            self.contact_book.names_tuple
        )
        contact = self.contact_book.get_contact(name.value)
        birthday = self.validated_input(
            Date,
            "User birthday in YYYY-MM-DD format, empty to skip: ",
            allow_empty=True
        )
        if birthday is None:
            return "Nothing has been changed"
        contact.birthday = birthday.value
        return f"User birthday has been changed to {birthday.value}"

    @command_handler("search", "Search by pattern in any record")
    def search_command(self):
        pattern = prompt("Search: ").strip()
        result = self.contact_book.find(pattern)
        if not result:
            return "Nothing found"
        return "\n\n".join(str(contact) for contact in result)

    @command_handler("show", "Show all records in contact book")
    def show_command(self):
        if not self.contact_book.data:
            return "It's empty. There are no any records."
        return "\n" + "\n\n".join(
            str(contact) for contact in self.contact_book.data
        )

    @command_handler("notes show", "Show all notes in notes book")
    def show_notes_command(self):
        if not self.notes_book.data:
            return "It's empty. There are no any records."
        return "\n" + "\n\n".join(str(note) for note in self.notes_book.data)

    @command_handler("note add", "Add note to notes book")
    def add_note_command(self):
        title = self.validated_input(Title, "Note title: ")
        text = self.validated_input(Text, "Note text: ")
        tag = self.validated_input(
            Tag,
            "Note tag: ",
            self.notes_book.notes_tags_set
        )
        note = Note(title.value, text.value, tag.value)
        self.notes_book.add_record(note)
        return f"Note with title {title} has been added"

    @command_handler("note add tag", "Add tag to note")
    def add_tag_command(self):
        title = self.validated_input(
            Title,
            "Note title: ",
            self.notes_book.titles_tuple
        )
        note = self.notes_book.get_note(title.value)
        tag = self.validated_input(
            Tag,
            "Note tag: ",
            self.notes_book.notes_tags_set
        )
        note.add_tag(tag.value)
        return "Note has been updated"

    @command_handler("note remove tag", "Remove tag from note")
    def rm_tag_command(self):
        title = self.validated_input(
            Title,
            "Note title: ",
            self.notes_book.titles_tuple
        )
        note = self.notes_book.get_note(title.value)
        tag = self.validated_input(
            Tag,
            "Note tag: ",
            note.tags_set
        )
        note.remove_tag(tag.value)
        return "Note has been updated"

    @command_handler("note edit tag", "Edit note tag")
    def edit_tag_command(self):
        title = self.validated_input(
            Title,
            "Note title: ",
            self.notes_book.titles_tuple
        )
        note = self.notes_book.get_note(title.value)
        tag = self.validated_input(Tag, "Note tag: ", note.tags_set)
        new_tag = self.validated_input(
            Tag,
            "New note tag: ",
            self.notes_book.notes_tags_set
        )
        note.change_tag(tag.value, new_tag.value)
        return "Note has been updated"

    @command_handler("note remove", "Remove note from notes book")
    def rm_note_command(self):
        title = self.validated_input(
            Title,
            "Note title: ",
            self.notes_book.titles_tuple
        )
        self.notes_book.delete(title.value)
        return f"Note with title {title} has been removed"

    @command_handler("note search", "Notes search by pattern")
    def search_note_command(self):
        pattern = prompt("Search: ").strip()
        result = self.notes_book.find(pattern)
        if not result:
            return "Nothing found"
        return "\n\n".join(str(note) for note in result)

    @command_handler("note tag search", "Notes search by tag")
    def search_note_tag_command(self):
        tag = self.validated_input(
            Tag,
            "Note tag: ",
            self.notes_book.notes_tags_set
        )
        result = self.notes_book.find(tag.value, tag_only=True)
        if not result:
            return "Nothing found"
        return "\n\n".join(str(note) for note in result)

    @command_handler("sort folder", "Smart file sorter")
    def sort_command(self):
        path = Path()
        dir_list = filter(lambda dir: dir.is_dir(), path.iterdir())
        dir_list = tuple(dirs.stem for dirs in dir_list)
        dir_path = self.validated_input(
            Path,
            "Path to folder, empty to skip: ",
            dir_list,
            allow_empty=True
        )
        if dir_path is None:
            return "Nothing has been changed"
        init_folder(dir_path)
        return f"Folder {dir_path.absolute()} has been sorted"

    @command_handler(
            "birthday persons",
            "Birthday persons list to specific date"
    )
    def birthday_command(self):
        days = prompt("Number of days from today: ").strip()
        if not days.isdigit():
            raise ValueError("Incorrect input. Should be number.")
        result = self.contact_book.days_to_birthday(int(days))
        if not result:
            return "Nothing found"
        return "\n\n".join(str(contact) for contact in result)

    def main_loop(self):
        print(f"\n{self.help()}")
        while self.running:
            command_completer = WordCompleter(commands)
            command = prompt('>>> ', completer=command_completer)
            command = command.lower().strip()
            if command not in commands:
                print("No such command")
                continue
            print(commands[command][0](self))
