"""
Contains class definition for a Container
"""


class Container:
    """A class to represent a container and the valid operations on a container"""

    description = "{EMPTY}"
    location = (0, 0)
    weight = 0

    def __init__(self, location, weight, description) -> None:
        self.location = location
        self.weight = weight
        self.description = description

    def move(self, column):
        pass
