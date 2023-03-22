"""
Contains class definition for a Container
"""


class Container:
    """A class to represent a container data"""

    def __init__(self, weight=0, description="EMPTY", on_ship=True):
        self.weight = weight
        self.description = description
        self.on_ship = on_ship

    def get_description(self) -> str:
        """Returns the container's description as in the manifest"""
        return self.description

    def get_weight(self) -> int:
        return self.weight

    def is_on_ship(self) -> int:
        return self.on_ship

    def __repr__(self):
        return "[%s, %s]" % (self.description, self.on_ship)

    def __str__(self):
        return "%s" % self.description

    def manifest_format(self, row, column) -> str:
        return "[%02d, %02d], {%05d}, %s]" % (9 - row, column, self.weight, self.description)

    def __eq__(self, __o) -> bool:
        return isinstance(__o, Container) and self.description == __o.description
