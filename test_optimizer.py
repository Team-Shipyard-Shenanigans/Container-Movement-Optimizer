"""
Module for testing the optimizer class
"""
import pytest as pt
import optimizer as Optimizer
import grid as Grid
import container as Container


def test_get_containers():
    bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    o = Optimizer.Optimizer(bay, buffer)

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

    retrieved = o.get_containers(Container.Container(weight=88, description="Ralphs"))

    assert len(retrieved) == 0

    retrieved = o.get_containers(Container.Container(description="Frice"))

    assert len(retrieved) == 1

    assert retrieved[0].get_description() == "Frice"

    assert retrieved[0].get_weight() == 520

    retrieved = o.get_containers(Container.Container(description="Costco"))

    assert len(retrieved) == 3

    for i in retrieved:
        assert i.get_description() == "Costco"

        assert i.get_weight() == 996

    retrieved = o.get_containers(Container.Container(description="Walmart"))

    assert len(retrieved) == 2

    prev = 0
    for i in retrieved:
        assert i != prev
        assert i.get_description() == "Walmart"
        assert i.get_weight() == 333
        prev = i


def test_move_to_column():
    bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    o = Optimizer.Optimizer(bay, buffer)

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

    origin, dest = o.move_to_column(1, 3)

    assert bay.get_stacks(1) == origin

    assert origin.get_height() == 2

    assert origin.pop() == c2

    assert bay.get_stacks(3) == dest

    assert dest.get_height() == 1

    assert dest.pop() == c3


def test_column_move_cost():
    bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    o = Optimizer.Optimizer(bay, buffer)

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

    cost, stack, height = o.column_move_cost(1)

    assert cost == 2

    assert stack.get_column() == 2

    assert height == 3

    cost, stack, height = o.column_move_cost(2)

    assert cost == 2

    assert stack.get_column() == 1

    assert height == 3

    with pt.raises(ValueError):
        o.column_move_cost(0)

    bay.clear_bay()

    c1.move((7, 1))
    c2.move((6, 1))
    c3.move((5, 1))
    c4.move((7, 3))
    c5.move((6, 3))
    c6.move((7, 4))

    for i in cont_list:
        bay.add_container(i)

    bay.convert_grid_to_stack()

    cost, stack, height = o.column_move_cost(1)

    assert cost == 2

    assert stack.get_column() == 3

    assert height == 3

    cost, stack, height = o.column_move_cost(3)

    assert cost == 1

    assert stack.get_column() == 4

    assert height == 2

    cost, stack, height = o.column_move_cost(4)

    assert cost == 1

    assert stack.get_column() == 5

    assert height == 1
