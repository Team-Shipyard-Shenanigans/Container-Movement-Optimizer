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

    container.move((8, 1), True)

    assert container.get_cost((4, 22)) == 4 + 21

    container.move((10, 10), True)

    assert container.get_cost((9, 1)) == 1 + 9

    container.move((12, 9), True)

    assert container.get_cost((0, 0)) == 12 + 9


def test_move():
    """
    Tests the move function
    """

    cont = c.Container()

    loc1 = (0, 1)
    loc2 = (8, 5)
    loc3 = (3, 9)

    cont.move(loc1, False)
    assert cont.get_location() == (0, 1) and not cont.is_on_ship()

    cont.move(loc2, True)
    assert cont.get_location() == (8, 5) and cont.is_on_ship()

    cont.move(loc3, False)
    assert cont.get_location() == (3, 9) and not cont.is_on_ship()
