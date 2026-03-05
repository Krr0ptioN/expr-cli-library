
from commands import (
    CreateTaskCommandHandler,
)

class CommandPrompt:
    __commands = {
        "create-task": CreateTaskCommandHandler,
    }

    parse_command_input()

    def prompt_loop():
        while True:
            command = input("-> ")
            if command in commands.keys():
                commands[command]()

def main():
    cmdBus = CommandPrompt()
    cmdBus.prompt_loop()



if __name__ == "__main__":
    main()
