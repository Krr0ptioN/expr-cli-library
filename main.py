
def createTask():
    title = input("Enter task's title: ")
    descrption = input("Enter task's descrption: ")
    status = "TODO"
    print(f"\n[{status}] {title}: {descrption}")

def editTask():
    print("editing task")

def main():
    commands = {
        "create-task": createTask,
        "edit-task": editTask,
    }

    while True:
        command = input("-> ")
        if command in commands.keys():
            commands[command]()



if __name__ == "__main__":
    main()
