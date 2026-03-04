
def createTaskCommandHandler():
    title = input("Enter task's title: ")
    descrption = input("Enter task's descrption: ")
    status = "TODO"
    print(f"\n[{status}] {title}: {descrption}")

def editTaskCommandHandler():
    print("editing task")

def main():
    commands = {
        "create-task": createTaskCommandHandler,
        "edit-task": editTaskCommandHandler,
    }

    while True:
        command = input("-> ")
        if command in commands.keys():
            commands[command]()



if __name__ == "__main__":
    main()
