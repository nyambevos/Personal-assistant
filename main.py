""" Файл запуску програми"""

from assistant.assistant import Assistant


def main():
    assistant = Assistant()
    assistant.main_loop()


if __name__ == "__main__":
    main()