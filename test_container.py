"""
Module for testing the Container class
"""
import container as c


def test_get_cost():
    """
    Tests the get_cost function
    """
    container = c.Container()

    assert container.get_cost((0, 1)) == 1

    container.move((8, 1))

    assert container.get_cost((4, 22)) == 4 + 21

    container.move((10, 10))

    assert container.get_cost((9, 1)) == 1 + 9

    container.move((12, 9))

    assert container.get_cost((0, 0)) == 12 + 9
