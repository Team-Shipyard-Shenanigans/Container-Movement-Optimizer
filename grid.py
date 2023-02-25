"""
An interface for grid objects like Buffer and ShipBay
"""
from abc import ABC, abstractmethod
import container as Container


class Grid(ABC):
    """
    An interface for grid objects like Buffer and ShipBay
    """

    @abstractmethod
    def index_mapper(self, value):
        """
        Abstract method for subclasses of the grid class to specify their own mapping
        """


class Buffer(Grid):
    """
    The class representing the buffer with appropriate grid size.
    """

    grid = []

    def __init__(self):
        pass

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

    grid = []

    def __init__(self):
        pass

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

    def add_container(self, container=Container.Container()):
        """Adds given container to the location specified by the container."""
        indices = container.get_location()
        self.grid[indices[0]][indices[1]] = container

    def move_container(self, container=Container.Container(), column=0):

        
        
        
