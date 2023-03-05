"""
Module for testing the Grid class and its subclasses
"""
import grid, container as Container


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


def test_convert_to_stacks():
    bay = grid.ShipBay()

    c1 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c2 = Container.Container(weight=996, description="Costco", on_ship=True)
    c3 = Container.Container(weight=996, description="Costco", on_ship=True)
    c4 = Container.Container(weight=996, description="Costco", on_ship=True)
    c5 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c6 = Container.Container(weight=520, description="Frice", on_ship=True)

    cont_list = [c1, c2, c3, c4, c5, c6]

    c1.move((7, 1))
    c2.move((6, 1))
    c3.move((5, 1))
    c6.move((7, 2))
    c5.move((6, 2))
    c4.move((5, 2))

    for i in cont_list:
        bay.add_container(i)

    bay.convert_grid_to_stack()

    assert bay.get_stacks()[1].pop() == c3
    assert bay.get_stacks()[1].pop() == c2
    assert bay.get_stacks()[1].pop() == c1

    assert bay.get_stacks()[2].pop() == c4
    assert bay.get_stacks()[2].pop() == c5
    assert bay.get_stacks()[2].pop() == c6

    for i in {0, 3, 4, 5, 6, 7}:
        assert bay.get_stacks(i).get_height() == 0
