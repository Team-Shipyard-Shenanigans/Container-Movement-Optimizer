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

    def __init__(self, rows=0, columns=0):
        self.grid = [[None] * columns for i in range(rows)]
        self.stacks = []
        self.rows = rows
        self.columns = columns

    @abstractmethod
    def index_mapper(self, value) -> tuple[int, int]:
        """
        Abstract method for subclasses of the grid class to specify their own mapping
        """

    @abstractmethod
    def index_unmap(self, location) -> int:
        """
        Abstract method for subclasses of the grid class to specify their own unmapping
        """

    def get_stacks(self, column=None) -> list["Stack.Stack"]:
        return self.stacks if column is None else self.stacks[column]

    def get_grid(self) -> list[list["Container.Container"]]:
        return self.grid

    def add_container(self, container=Container.Container(), row=0, column=0):
        """Adds given container to the location specified by the container."""
        self.grid[row][column] = container

    def convert_grid_to_stack(self):
        for j in range(self.columns):
            stack = Stack.Stack(j, self.rows)
            for i in range(self.rows - 1, -1, -1):
                cont = self.grid[i][j]
                if cont is not None:
                    stack.push(cont)
            self.stacks.append(stack)

    def get_container(self, row_index, col_index) -> "Container.Container":
        return self.grid[row_index][col_index]

    def clear_bay(self):
        self.grid = [[None] * self.columns for i in range(self.rows)]
        self.stacks = []

    def __repr__(self) -> str:
        return "Rows: %s Columns: %s Contents: %s" % (self.rows, self.columns, self.grid)

    def __str__(self) -> str:
        string = ""
        for i in self.grid:
            for j in i:
                string = string + " %s " % (j)
            string = string + "\n"
        return string

    def move_to_column(self, origin_column, dest_column, container=None):
        if dest_column != -1 and origin_column != -1:
            origin_stack = self.stacks[origin_column]
            dest_stack = self.stacks[dest_column]
            origin_row = origin_stack.get_max_height() - origin_stack.get_height()
            dest_row = dest_stack.get_max_height() - (dest_stack.get_height() + 1)
            cont = origin_stack.pop()
            dest_stack.push(cont)

            self.grid[origin_row][origin_column] = None
            self.grid[dest_row][dest_column] = cont
        elif dest_column == -1 and origin_column != -1:
            origin_stack = self.stacks[origin_column]
            origin_row = origin_stack.get_max_height() - origin_stack.get_height()
            origin_stack.pop()
            self.grid[origin_row][origin_column] = None
        elif dest_column != -1 and origin_column == -1 and container is not None:
            dest_stack = self.stacks[dest_column]
            dest_row = dest_stack.get_max_height() - (dest_stack.get_height() + 1)
            dest_stack.push(container)
            self.grid[dest_row][dest_column] = container
        else:
            raise ValueError("Cannot move to non_existing column from non_existing column")

    def contains_any(self, containers) -> bool:
        for container in containers:
            for i in self.grid:
                for j in i:
                    if j is not None and j.get_description() == container.get_description():
                        return True
        return False

    def contains_all(self, containers) -> bool:
        for container in containers:
            has_cont = False
            for i in self.grid:
                for j in i:
                    if j is not None and j.get_description() == container.get_description():
                        has_cont = True
            if has_cont is False:
                return False
        return True

    def get_height(self) -> int:
        return self.rows

    def get_containers(self, container=Container.Container()) -> list[tuple["Container.Container", int]]:
        """Gets all target containers based on description"""
        container_array = []
        for i in enumerate(self.grid):
            for j in enumerate(i[1]):
                if j[1] is not None and j[1].get_description() == container.get_description():
                    container_array.append(j)
        return container_array

    def remove_container(self, row, column):
        self.grid[row][column] = None
        self.convert_grid_to_stack()

    def __eq__(self, __o: object) -> bool:
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if self.grid[i][j] != __o.grid[i][j]:
                    return False
        return True

    def manhattan(self, origin, destination) -> int:
        origin_row = origin[0]
        origin_col = origin[1]
        dest_row = destination[0]
        dest_col = destination[1]
        return abs(origin_row - dest_row) + abs(origin_col - dest_col)

    def get_columns(self) -> int:
        return self.columns

    def get_rows(self) -> int:
        return self.rows


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

    def index_unmap(self, location) -> int:  ## 95 -> 3, 23, 3 * 24 = 72 + 23 = 95
        return (location[0] * 24) + location[1]

    def __deepcopy__(self, memo):
        new_grid = Buffer()
        for i in range(self.rows):
            for j in range(self.columns):
                new_grid.grid[i][j] = self.grid[i][j]
        new_grid.convert_grid_to_stack()
        return new_grid


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

    def index_unmap(self, location) -> int:  ## 95 -> 3, 23, 3 * 24 = 72 + 23 = 95
        return (location[0] * 12) + location[1]

    def __deepcopy__(self, memo):
        new_grid = ShipBay()
        for i in range(self.rows):
            for j in range(self.columns):
                new_grid.grid[i][j] = self.grid[i][j]
        new_grid.convert_grid_to_stack()
        return new_grid
