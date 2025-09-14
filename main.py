import json

class Task:
    def __init__(self, title, deadline=None, completed=False):
        self.title = title
        self.deadline = deadline
        self.completed = completed
    
    def __str__(self):
        status = "✅ Done." if self.completed else "❌ Not yet completed."
        date = self.deadline if self.deadline else "Undefined!"
        return f"Task: {self.title}\nDeadline: {date}\nStatus: {status}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "completed": self.completed
        }
    
    @staticmethod
    def from_dict(data):
        return Task(data["title"], data.get("deadline"), data.get("completed", False))


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()
    
    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()
    
    def remove_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks.pop(task_number - 1)
            self.save_tasks()
            return True
        return False        
    
    def mark_completed(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1].completed = True
            self.save_tasks()
            return True
        return False
    
    def show_tasks(self):
        for index, task in enumerate(self.tasks):
            print(f"Task {index + 1}:")
            print(task)
            print("-" * 50)

        if len(self.tasks) == 0:
            print("There is no tasks to display!")

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            self.tasks = []


manager = TaskManager()

def get_task_number(action):
    try:
        return int(input(f"Enter task number to {action}: "))
    except ValueError:
        print("Please enter a valid task number.")
        return None

def add_task():
    title = input("Task title: ")
    deadline = input("Task deadline: ")
    task = Task(title, deadline)
    manager.add_task(task)
    print("Task Added successfully.")

def remove_task():
    if not manager.tasks:
        print("No tasks to remove.")
        return
    manager.show_tasks()
    task_number = get_task_number("remove")
    if task_number is None:
        return
    if manager.remove_task(task_number):
        print("Task removed successfully.")
    else:
        print("Task number is out of range!")

def mark_completed():
    if not manager.tasks:
        print("No tasks to mark.")
        return
    manager.show_tasks()
    task_number = get_task_number("mark as completed")
    if task_number is None:
        return
    if manager.mark_completed(task_number):
        print("Task completed.")
    else:
        print("Task number is out of range!")

def show_tasks():
    manager.show_tasks()

def main():
    while True:
        print("### Task Manager ###")
        print("1- Add new task.")
        print("2- Remove task.")
        print("3- Mark task as completed.")
        print("4- Show tasks.")
        print("5- Exit.")
        print("What would you like to do (pick a number)? ")

        try:
            number = int(input())
        except ValueError:
            print("Please enter a valid number.")
            continue

        if number == 1:
            add_task()
        elif number == 2:
            remove_task()
        elif number == 3:
            mark_completed()
        elif number == 4:
            show_tasks()
        elif number == 5:
            break
        else:
            print("Please choose a correct number from 1 to 5.")
            continue


if __name__ == "__main__":
    main()