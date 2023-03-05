from abc import ABC


class Stack(ABC):
    containers = []
    column = 0
    max_height = 0

    def __init__(self, column, max_height):
        self.column = column
        self.max_height = max_height
        self.containers = []

    def pop(self):
        return self.containers.pop()

    def get_height(self):
        return len(self.containers)

    def push(self, container):
        if len(self.containers) < self.max_height:
            container.move((self.max_height - 1 - len(self.containers), self.column))
            self.containers.append(container)
        else:
            raise IndexError("Can only stack containers up to 8 high in ship bay")

    def get_column(self):
        return self.column

    def __repr__(self):
        return "[Column: %s, Height: %s, Contents: %s]" % (self.column, self.get_height(), self.containers)
