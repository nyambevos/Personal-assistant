from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
# from termcolor import colored
from colored import Fore, Style
from assistant.fields import *
from assistant.records import *
import textwrap

""" Модуль персонального асистента """

"""
“Персональний помічник” повинен вміти:
зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
виводити список контактів, у яких день народження через задану кількість днів від поточної дати;
перевіряти правильність введеного номера телефону та email під час створення або редагування запису та повідомляти користувача у разі некоректного введення;
здійснювати пошук контактів серед контактів книги;
редагувати та видаляти записи з книги контактів;
зберігати нотатки з текстовою інформацією;
проводити пошук за нотатками;
редагувати та видаляти нотатки;
додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
здійснювати пошук та сортування нотаток за ключовими словами (тегами);
сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).

"""


commands = {}

notes_book = [] # remove me!

# remove me too!!!
note = Note(
    "Daiquiri",
    "60 ml white Cuban rum, 20 ml fresh lime juice, 2 bar spoons superfine sugar. In a cocktail shaker add all ingredients. Stir well to dissolve the sugar. Add ice and shake. Strain into chilled cocktail glass.",
    "Cocktail"
)
note.add_tag("Daiquiri")
note.add_tag("Rum")
notes_book.append(note)

note = Note(
    "Martini",
    "60 mL (2.0 US fl oz) gin, 10 mL (0.34 US fl oz) dry vermouth. Pour all ingredients into mixing glass with ice cubes. Stir well. Strain into chilled martini cocktail glass.",
    "Cocktail"
)
note.add_tag("Martini")
note.add_tag("Gin")
note.add_tag("Vermouth")
notes_book.append(note)

note = Note(
    "Cosmopolitan",
    "40 ml Vodka Citron, 15 ml Cointreau, 15 ml Fresh lime juice, 30 ml cranberry juice. Shake all ingredients in cocktail shaker filled with ice. Strain into a large cocktail glass. Garnish with lime slice.",
    "Cocktail"
)
note.add_tag("Cosmopolitan")
note.add_tag("Vodka")

notes_book.append(note)



notes_book.append(note)

contact_book=[]

contact = Contact("Madilyn")
contact.add_phone("3569321443")
contact.add_phone("3605392707")
contact.add_phone("7922432903")
contact.birthday = "2002-07-07"
contact.email = "example@email.com"
contact.address = "5780 Kozey Garden, West Margeneville, OK 65613"
contact_book.append(contact)

contact = Contact("Roland")
contact.add_phone("5246670975")
contact.add_phone("1662428392")
contact.birthday = "1993-09-20"
contact.email = "example2@email.com"
contact.address = "573 Jones Forest, Port Nelida, AK 66734"
contact_book.append(contact)

contact = Contact("Julia")
contact.add_phone("1962802250")
contact.add_phone("9276019428")
contact.add_phone("5244315630")
contact.birthday = "1988-08-26"
contact.email = "example@email.com"
contact.address = "Suite 787 7328 Krajcik Bypass, New Jesston, WY 7362-91147"
contact_book.append(contact)


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
            except (ValueError, IndexError) as err:
                return f"{Fore.red}{err}{Style.reset}"
        commands[command] = (wrapper, description)
        return wrapper
    return input_error


class Assistant:
    def __init__(self) -> None:
        self.running = True

    @staticmethod
    def validated_input(cls, request, completer = None):
        inp_completer = WordCompleter(completer) if completer else None
        while True:
            try:
                inp = prompt(request, completer=inp_completer).strip()
                if not inp:
                    return None
                return cls(inp)
            except (ValueError, IndexError) as err:
                print(f"{Fore.red}{err}{Style.reset}")

    @command_handler("help", "Help")
    def help(self):
        return "Usage: type a command "\
            "or press TAB to command menu\n"\
            "list - list all commands"

    @command_handler("list", "List all commands")
    def list_command(self):
        return "\n".join(
            f"{command: <10}{val[1]}" for command, val in commands.items()
        )

    @command_handler("exit", "Exit")
    def exit_command(self):
        self.running = False
        return "Bye!"

    @command_handler("add", "Add new user to contact book")
    def add_command(self):
        name = self.validated_input(Name, "User name: ")
        phone = self.validated_input(Phone, "User phone, empty to skip: ")
        email = self.validated_input(
            EmailAddress,
            "User e-mail, empty to skip: "
        )
        birthday = self.validated_input(Date, "User birthday, empty to skip: ")
        return f"New user {name} has been added\n"\
            f"Phone: {phone}\n"\
            f"E-mail: {email}\n"\
            f"Birthday: {birthday}"
    
    @command_handler("remove", "Remove user from contact book")
    def remove_command(self):
        return "This is command placeholder"
    
    @command_handler("phone", "Add phone number to existing user")
    def phone_command(self):
        return "This is command placeholder"
    
    @command_handler("edit", "Edit existing user")
    def edit_command(self):
        return "This is command placeholder"
    
    @command_handler("search", "Search by pattern in any record")
    def search_command(self):
        return "This is command placeholder"
    
    @command_handler("show", "Show all records in contact book")
    def show_command(self):
        return "\n\n".join(str(contact) for contact in contact_book)
    
    @command_handler("notes show", "Show all notes in notes book")
    def show_notes_command(self):
        if not notes_book:
            return "It's empty. There are no any records."
        return "\n\n".join(str(note) for note in notes_book)
    
    @command_handler("note add", "Add note to notes book")
    def add_note_command(self):
        title = self.validated_input(Title, "Note title: ")
        text = self.validated_input(Text, "Note text: ")

        tags_autofill = set()
        for note in notes_book:
            tags_autofill.update(note.tags_set)

        tag = self.validated_input(Tag, "Note tag: ", tags_autofill)
        note = Note(title.value, text.value, tag.value)
        notes_book.append(note)
        return f"Note with title {title} has been added"
    
    @command_handler("note add tag", "Add tag to note")
    def add_tag_command(self):
        
        title_autofill = set()
        for note in notes_book:
            title_autofill.add(note.title.value)
        
        title = self.validated_input(Title, "Note title: ", title_autofill)

        tags_autofill = set()
        for note in notes_book:
            tags_autofill.update(note.tags_set)
            
        for note in notes_book:
            if note.title.value == title.value:
                break

        tag = self.validated_input(Tag, "Note tag: ", tags_autofill)
        note.add_tag(tag.value)
        return "Note has been updated"

    @command_handler("note remove tag", "Remove tag from note")
    def rm_tag_command(self):
        title_autofill = set()
        for note in notes_book:
            title_autofill.add(note.title.value)
        
        title = self.validated_input(Title, "Note title: ", title_autofill)

        for note in notes_book:
            if note.title.value == title.value:
                break

        tag = self.validated_input(Tag, "Note tag: ", note.tags_set)
        note.remove_tag(tag.value)
        return "Note has been updated"
    
    @command_handler("note edit tag", "Remove tag from note")
    def rm_tag_command(self):
        title_autofill = set()
        for note in notes_book:
            title_autofill.add(note.title.value)
        
        title = self.validated_input(Title, "Note title: ", title_autofill)

        for note in notes_book:
            if note.title.value == title.value:
                break

        tag = self.validated_input(Tag, "Note tag: ", note.tags_set)
        new_tag = self.validated_input(Tag, "Note tag: ")
        note.change_tag(tag.value, new_tag.value)
        return "Note has been updated"

    @command_handler("note remove", "Remove note from notes book")
    def rm_note_command(self):
        title_autofill = set()
        for note in notes_book:
            title_autofill.add(note.title.value)
        
        title = self.validated_input(Title, "Note title: ", title_autofill)

        for index, note in enumerate(notes_book):
            if note.title.value == title.value:
                break
        
        notes_book.pop(index)

        return f"Note with title {title} has been removed"
        
    
    @command_handler("sort folder", "Smart file sorter")
    def sort_command(self):
        return "This is command placeholder"

    @command_handler("birthday", "Birthday persons list to specific date")
    def birthday_command(self):
        return "This is command placeholder"
    
    def main_loop(self):
        print(self.help())
        while self.running:
            command_completer = WordCompleter(commands)
            command = prompt('>>> ', completer=command_completer)
            command = command.lower().strip()

            if command not in commands:
                print("No such command")
                continue

            print(commands[command][0](self))
