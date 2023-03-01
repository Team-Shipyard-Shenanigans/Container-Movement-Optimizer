from abc import ABC


class Stack(ABC):
    containers = []
    column = 0
    max_height = 0

    def __init__(self, column, max_height):
        self.column = column
        self.max_height = max_height

    def pop(self):
        return self.containers.pop()

    def height(self):
        return len(self.containers)

    def push(self, container):
        if len(self.containers) < self.max_height:
            container.move((self.max_height - len(self.containers), self.column))
            self.containers.append(container)
        else:
            raise IndexError("Can only stack containers up to 8 high in ship bay")
