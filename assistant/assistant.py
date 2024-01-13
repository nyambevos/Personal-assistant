from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from termcolor import colored
from assistant.fields import *

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
            except ValueError as err:
                return colored(err, "red")
        commands[command] = (wrapper, description)
        return wrapper
    return input_error


class Assistant:
    def __init__(self) -> None:
        self.running = True

    def validated_input(self, cls, request):
        while True:
            try:
                inp = prompt(request).strip()
                if not inp:
                    return None
                return cls(inp)
            except ValueError as err:
                print(colored(err, "red"))

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
        return "This is command placeholder"
    
    @command_handler("note", "Add note no notes book")
    def note_command(self):
        return "This is command placeholder for notes"
    
    @command_handler("remove note", "Remove note from notes book")
    def rm_note_command(self):
        return "This is command placeholder for notes"
    
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
            command = prompt('>>>', completer=command_completer)
            command = command.lower().strip()

            if command not in commands:
                print("No such command")
                continue

            print(commands[command][0](self))
