import random as rand
from enum import Enum 
import string

def taskHashId(title:str):
    random_character1 = rand.choice(string.ascii_letters)
    random_character2 = rand.choice(string.ascii_letters)
    random_character3 = rand.choice(string.ascii_letters)

    return title.rstrip() + random_character1 + random_character2 + random_character3

class TaskStatus(Enum)
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
    title: str
    description: str
    status: TaskStatus

    def __init__(self, title: str, descrption: str = ""):
        self.title = title
        self.description = descrption
        self.status = TaskStatus.TODO

class Store:
    file_storage = ""
    __tasks = { }

    def __init__(self, file_backup: str):
        self.file_storage = file_backup
        

    def save(self):
        with open(self.file_storage) as file:


    def addTask(self, newTask: Task):
        self.__tasks[taskHashId(title)] = newTask


def createTaskCommandHandler(store: Store, ):
    title = input("Enter task's title: ")
    descrption = input("Enter task's descrption: ")

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
