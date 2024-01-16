if __package__ is None or __package__ == '':
    from assistant.assistant import Assistant
else:
    from .assistant import Assistant

NICE_LOGO = r"""
______      _                  _   _____ _       _
|  _  \    (_)                (_) /  __ \ |     | |
| | | |__ _ _  __ _ _   _ _ __ _  | /  \/ |_   _| |__
| | | / _` | |/ _` | | | | '__| | | |   | | | | | '_ \
| |/ / (_| | | (_| | |_| | |  | | | \__/\ | |_| | |_) |
|___/ \__,_|_|\__, |\__,_|_|  |_|  \____/_|\__,_|_.__/
                 | |
                 |_|
"""


def main():
    # nice and useless intro
    print(NICE_LOGO)
    print("Present\n")
    print("Personal assistant")

    assistant = Assistant()
    assistant.load()
    assistant.main_loop()
    assistant.save()


if __name__ == "__main__":
    main()
