"""
Contains class definition for a Container
"""


class Container:
    """A class to represent a container and the valid operations on a container"""

    description = "{EMPTY}"
    location = (0, 0)
    weight = 0

    def __init__(self, location=(0, 0), weight=0, description="{EMPTY}") -> None:
        self.location = location
        self.weight = weight
        self.description = description

    def move(self, location):
        """Updates location to new value"""
        self.location = location

    def get_location(self):
        """Gets the current container's location"""
        return self.location

    def get_cost(self, location):
        """Returns the Manhattan distance cost of a movement from the container's current location to a destination"""
        return abs(self.location[0] - location[0]) + abs(self.location[1] - location[1])
