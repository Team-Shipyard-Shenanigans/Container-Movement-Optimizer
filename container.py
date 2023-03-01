"""
Contains class definition for a Container
"""


class Container:
    """A class to represent a container and the valid operations on a container"""

    description = "{EMPTY}"
    location = (0, 0)
    weight = 0
    on_ship = True

    def __init__(self, weight=0, description="{EMPTY}", on_ship=True) -> None:
        self.weight = weight
        self.description = description
        self.on_ship = on_ship

    def move(self, location):
        """Updates location to new value"""
        self.location = location

    def get_location(self):
        """Gets the current container's location"""
        return self.location

    def get_description(self):
        """Returns the container's description as in the manifest"""
        return self.description

    def get_cost(self, location):
        """Returns the Manhattan distance cost of a movement from the container's current location to a destination"""
        return abs(self.location[0] - location[0]) + abs(self.location[1] - location[1])

    def is_on_ship(self):
        return self.on_ship