import queue

class Scheduler:
    def __init__(self):
        self.task_queue = queue.Queue()

    def add_task(self, task):
        """Adds a task to the queue."""
        self.task_queue.put(task)
        print(f"Task added to the queue: {task}")

    def get_task(self):
        """Gets a task from the queue."""
        if not self.task_queue.empty():
            return self.task_queue.get()
        return None
