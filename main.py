
class ToDoApp:
    def __init__(self):
        self.tasks = []
        self.commands_history = []
        self.history_index = 0

    def _record_command(self, command):
        if self.history_index < len(self.commands_history):
            self.commands_history = self.commands_history[:self.history_index]
        self.commands_history.append(command)
        self.history_index += 1

    def _replay_history(self):
        self.tasks = []
        for cmd in self.commands_history[:self.history_index]:
            if cmd["type"] == "add":
                self.tasks.append({"text": cmd["text"], "completed": False})
            elif cmd["type"] == "remove":
                idx = cmd["index"] - 1
                if 0 <= idx < len(self.tasks):
                    self.tasks.pop(idx)
            elif cmd["type"] == "toggle":
                idx = cmd["index"] - 1
                if 0 <= idx < len(self.tasks):
                    self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]

    def add_task(self, text):
        self.tasks.append({"text": text, "completed": False})
        self._record_command({"type": "add", "text": text})

    def remove_task(self, index):
        idx = index - 1
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            self._record_command({"type": "remove", "index": index})

    def toggle_task(self, index):
        idx = index - 1
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
            self._record_command({"type": "toggle", "index": index})

    def print_tasks(self):
        if not self.tasks:
            print("No tasks.")
        for i, task in enumerate(self.tasks, start=1):
            mark = "[✓]" if task["completed"] else "[ ]"
            print(f"{i}. {mark} {task['text']}")

    def undo(self):
        if self.history_index == 0:
            print("Nothing to undo.")
            return
        self.history_index -= 1
        self._replay_history()

    def redo(self):
        if self.history_index >= len(self.commands_history):
            print("Nothing to redo.")
            return
        self.history_index += 1
        self._replay_history()


    def parse_and_execute(self, user_input):
        parts = user_input.strip().split(" ", 1)
        cmd = parts[0].lower()
        if cmd == "add" and len(parts) > 1:
            self.add_task(parts[1])
            print (f'Added task: "{parts[1]}"')

        elif cmd == "remove" and len(parts) > 1 and parts[1].isdigit():
            self.remove_task(int(parts[1]))
            print (f'Removed task {parts[1]}')

        elif cmd == "toggle" and len(parts) > 1 and parts[1].isdigit():
            self.toggle_task(int(parts[1]))
            print (f'Toggled task {parts[1]}')

        elif cmd == "view":
            self.print_tasks()

        elif cmd == "undo":
            self.undo()
            self.print_tasks()
            print("Undid last action.")

        elif cmd == "redo":
            self.redo()
            self.print_tasks()
            print("Redid last action.")
            
        elif cmd == "exit":
            print("Goodbye!")
            return False
        else:
            print("Invalid command.")
        return True

def main():
    print("Welcome to your To-Do List!")
    app = ToDoApp()
    while True:
        user_input = input("what would you like to do? add/remove/toggle/view/undo/redo/exit: ")
        if not app.parse_and_execute(user_input):
            break

# TDD Style Tests

def test_add_task():
    app = ToDoApp()
    app.add_task("Test Task")
    assert len(app.tasks) == 1
    assert app.tasks[0]["text"] == "Test Task"
    assert not app.tasks[0]["completed"]

def test_toggle_task():
    app = ToDoApp()
    app.add_task("Task")
    app.toggle_task(1)
    assert app.tasks[0]["completed"] is True

def test_remove_task():
    app = ToDoApp()
    app.add_task("Task")
    app.remove_task(1)
    assert len(app.tasks) == 0

if __name__ == "__main__":
    tests = [test_add_task, test_toggle_task, test_remove_task]
    for test in tests:
        test()
    main()

