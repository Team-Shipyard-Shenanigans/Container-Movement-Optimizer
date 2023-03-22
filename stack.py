class Stack:
    containers = []
    column = 0
    max_height = 0

    def __init__(self, column, max_height):
        self.column = column
        self.max_height = max_height
        self.containers = []

    def pop(self):
        return self.containers.pop()

    def get_max_height(self):
        return self.max_height

    def get_height(self):
        return len(self.containers)

    def push(self, container, on_ship=None):
        if len(self.containers) < self.max_height:
            self.containers.append(container)
        else:
            raise IndexError("Can only stack containers up to %s high in current area" % (self.max_height))

    def peek(self):
        return self.containers[-1] if len(self.containers) != 0 else None

    def get_column(self):
        return self.column

    def __repr__(self):
        return "[Column: %s, Height: %s, Contents: %s]" % (self.column, self.get_height(), self.containers)
