"""
Module for testing the Grid class and its subclasses
"""
import grid


def test_index_mapper():
    """Tests whether the single dimensional scalar is correctly mapped to an index on the grid"""

    grid_type = grid.ShipBay()

    assert grid_type.index_mapper(95) == (7, 11)
    assert grid_type.index_mapper(0) == (0, 0)
    assert grid_type.index_mapper(60) == (5, 0)

    grid_type = grid.Buffer()

    assert grid_type.index_mapper(95) == (3, 23)
    assert grid_type.index_mapper(0) == (0, 0)
    assert grid_type.index_mapper(60) == (2, 12)
