"""
An interface for grid objects like Buffer and ShipBay
"""
from abc import ABC, abstractmethod
import container as Container
import stack as Stack


class Grid(ABC):
    """
    An interface for grid objects like Buffer and ShipBay
    """

    grid = None
    stacks = None
    rows = None
    columns = None

    def __init__(self, rows=0, columns=0):
        self.grid = [[None] * columns for i in range(rows)]
        self.stacks = []
        self.rows = rows
        self.columns = columns

    @abstractmethod
    def index_mapper(self, value):
        """
        Abstract method for subclasses of the grid class to specify their own mapping
        """

    def get_stacks(self, column=None):
        return self.stacks if column is None else self.stacks[column]

    def get_grid(self):
        return self.grid

    def add_container(self, container=Container.Container()):
        """Adds given container to the location specified by the container."""
        indices = container.get_location()
        self.grid[indices[0]][indices[1]] = container

    def convert_grid_to_stack(self):
        for j in range(self.columns):
            stack = Stack.Stack(j, self.rows)
            for i in range(self.rows - 1, -1, -1):
                cont = self.grid[i][j]
                if cont is not None:
                    stack.push(cont)
            self.stacks.append(stack)

    def clear_bay(self):
        self.grid = [[None] * self.columns for i in range(self.rows)]
        self.stacks = []

    def __repr__(self):
        return "Rows: %s Columns: %s Contents: %s" % (self.rows, self.columns, self.grid)


class Buffer(Grid):
    """
    The class representing the buffer with appropriate grid size.
    """

    def __init__(self):
        super().__init__(4, 24)

    def index_mapper(self, value):
        """
        Parameters: an integer
        Output: indices converted of the corresponding 4x24 matrix.
        """
        row_index = 0
        col_index = 0
        if value > 96:
            raise ValueError("Index out of bounds")

        if value == 96:
            row_index = -1
            col_index = -1
        else:
            row_index = int(value / 24)
            col_index = value % 24
        return (row_index, col_index)


class ShipBay(Grid):
    """
    The class representing the ship bay with appropriate grid size.
    """

    def __init__(self):
        super().__init__(8, 12)

    def index_mapper(self, value):
        """
        Parameters: an integer
        Output: indices converted of the corresponding 8x12 matrix.
        """
        row_index = 0
        col_index = 0
        if value > 96:
            raise ValueError("Index out of bounds")
        elif value == 96:
            row_index = -1
            col_index = -1
        else:
            row_index = int(value / 12)
            col_index = value % 12
        return (row_index, col_index)
