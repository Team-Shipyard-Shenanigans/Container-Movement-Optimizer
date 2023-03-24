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

    bay.add_container(c1, 7, 1)
    bay.add_container(c2, 6, 1)
    bay.add_container(c3, 5, 1)
    bay.add_container(c4, 7, 2)
    bay.add_container(c5, 6, 2)
    bay.add_container(c6, 5, 2)

    bay.convert_grid_to_stack()

    assert bay.get_stacks()[1].pop() == c3
    assert bay.get_stacks()[1].pop() == c2
    assert bay.get_stacks()[1].pop() == c1

    assert bay.get_stacks()[2].pop() == c6
    assert bay.get_stacks()[2].pop() == c5
    assert bay.get_stacks()[2].pop() == c4

    for i in {0, 3, 4, 5, 6, 7}:
        assert bay.get_stacks(i).get_height() == 0


def test_get_containers():
    bay = grid.ShipBay()

    c1 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c2 = Container.Container(weight=996, description="Costco", on_ship=True)
    c3 = Container.Container(weight=996, description="Costco", on_ship=True)
    c4 = Container.Container(weight=996, description="Costco", on_ship=True)
    c5 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c6 = Container.Container(weight=520, description="Frice", on_ship=True)

    bay.add_container(c1, 7, 1)
    bay.add_container(c2, 6, 1)
    bay.add_container(c3, 5, 1)
    bay.add_container(c4, 7, 2)
    bay.add_container(c5, 6, 2)
    bay.add_container(c6, 5, 2)

    retrieved = bay.get_containers(Container.Container(weight=88, description="Ralphs"))

    assert len(retrieved) == 0

    retrieved = bay.get_containers(Container.Container(description="Frice"))

    assert len(retrieved) == 1

    assert retrieved[0][1].get_description() == "Frice"

    assert retrieved[0][1].get_weight() == 520

    retrieved = bay.get_containers(Container.Container(description="Costco"))

    assert len(retrieved) == 3

    for i in retrieved:
        assert i[1].get_description() == "Costco"

        assert i[1].get_weight() == 996

    retrieved = bay.get_containers(Container.Container(description="Walmart"))

    assert len(retrieved) == 2

    prev = 0
    for i in retrieved:
        assert i != prev
        assert i[1].get_description() == "Walmart"
        assert i[1].get_weight() == 333
        prev = i


def test_eq():
    bay = grid.ShipBay()

    c1 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c2 = Container.Container(weight=996, description="Costco", on_ship=True)
    c3 = Container.Container(weight=996, description="Costco", on_ship=True)
    c4 = Container.Container(weight=996, description="Costco", on_ship=True)
    c5 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c6 = Container.Container(weight=520, description="Frice", on_ship=True)

    bay.add_container(c1, 7, 1)
    bay.add_container(c2, 6, 1)
    bay.add_container(c3, 5, 1)
    bay.add_container(c4, 7, 2)
    bay.add_container(c5, 6, 2)
    bay.add_container(c6, 5, 2)

    bay2 = grid.ShipBay()

    c1 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c2 = Container.Container(weight=996, description="Costco", on_ship=True)
    c3 = Container.Container(weight=996, description="Costco", on_ship=True)
    c4 = Container.Container(weight=996, description="Costco", on_ship=True)
    c5 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c6 = Container.Container(weight=520, description="Frice", on_ship=True)

    bay2.add_container(c1, 7, 1)
    bay2.add_container(c2, 6, 1)
    bay2.add_container(c3, 5, 1)
    bay2.add_container(c4, 7, 2)
    bay2.add_container(c5, 6, 2)
    bay2.add_container(c6, 5, 2)

    assert bay == bay2
