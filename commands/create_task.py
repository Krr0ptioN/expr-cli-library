from base import CommandHandler, Command

class CreateTaskCommand(Command):
    id: "create-task"
    command_name: "create-task"


class CreateTaskCommandHandler(CommandHandler):
    def handle(command: CreateTaskCommand):
        title = input("Enter task's title: ")
        descrption = input("Enter task's descrption: ")
        Task(title,descrption)

        print(f"\n[{status}] {title}: {descrption}")
