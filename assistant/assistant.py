from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from assistant.fields.date import Date

from assistant.fields.phone import Phone
from assistant.fields.email_address import EmailAddress


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
                return err
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
                print(err)

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
        name = prompt("User name: ").strip()
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
