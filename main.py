""" Файл запуску програми"""

from assistant.assistant import Assistant


def main():
    assistant = Assistant()
    assistant.load()
    assistant.main_loop()
    # assistant.save()


if __name__ == "__main__":
    main()