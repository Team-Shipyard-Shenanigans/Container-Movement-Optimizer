"""
Contains class definition for a Container
"""


class Container:
    """A class to represent a container and the valid operations on a container"""

    description = "EMPTY"
    location = (0, 0)
    weight = 0
    on_ship = True

    def __init__(self, weight=0, description="EMPTY", on_ship=True):
        self.weight = weight
        self.description = description
        self.on_ship = on_ship

    def move(self, location, on_ship=None):
        """Updates location to new value"""

        if on_ship != True is not on_ship is not False and on_ship is not None:
            raise ValueError("Error, on_ship can either be True, False, or -1 (use existing value)")

        self.location = location
        self.on_ship = self.on_ship if on_ship is None else on_ship

    def get_location(self):
        """Gets the current container's location"""
        return self.location

    def get_description(self):
        """Returns the container's description as in the manifest"""
        return self.description

    def get_cost(self, location):
        """Returns the Manhattan distance cost of a movement from the container's current location to a destination"""
        return abs(self.location[0] - location[0]) + abs(self.location[1] - location[1])

    def get_weight(self):
        return self.weight

    def is_on_ship(self):
        return self.on_ship

    def __repr__(self):
        return "[%s, %s, %s]" % (self.description, self.location, self.on_ship)

    def manifest_format(self):
        return "[%02d, %02d], \{%05d\}, %s]" % (9 - self.location[0], self.location[1], self.weight, self.description)
