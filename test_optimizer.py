"""
Module for testing the optimizer class
"""
import optimizer as Optimizer
import grid as Grid
import container as Container


def test_unload():
    manifest = open("case1.txt", "r", encoding="ascii")
    ship_bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    for line in manifest:
        line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        data = line.split(",")
        if str(data[3].strip()) != "UNUSED":
            row = ship_bay.get_height() - int(data[0])
            col = int(data[1]) - 1
            cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
            ship_bay.add_container(cont, row, col)

    ship_bay.convert_grid_to_stack()
    buffer.convert_grid_to_stack()

    o = Optimizer.Optimizer()

    cont = Container.Container(99, "Cat")

    return o.load(ship_bay, buffer, [], [cont])


def test_load():
    manifest = open("case2.txt", "r", encoding="ascii")
    ship_bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    for line in manifest:
        line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        data = line.split(",")
        if str(data[3].strip()) != "UNUSED":
            row = ship_bay.get_height() - int(data[0])
            col = int(data[1]) - 1
            cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
            ship_bay.add_container(cont, row, col)

    ship_bay.convert_grid_to_stack()
    buffer.convert_grid_to_stack()
    o = Optimizer.Optimizer()

    cont = Container.Container(431, "Bat")

    return o.load(ship_bay, buffer, [cont], [])


def test_load_unload():
    manifest = open("case3.txt", "r", encoding="ascii")
    ship_bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    for line in manifest:
        line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        data = line.split(",")
        if str(data[3].strip()) != "UNUSED":
            row = ship_bay.get_height() - int(data[0])
            col = int(data[1]) - 1
            cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
            ship_bay.add_container(cont, row, col)

    ship_bay.convert_grid_to_stack()
    buffer.convert_grid_to_stack()
    o = Optimizer.Optimizer()
    load = []
    load.append(Container.Container(532, "Bat"))
    load.append(Container.Container(6317, "Rat"))

    unload = []
    unload.append(Container.Container(100, "Cow"))

    return o.load(ship_bay, buffer, load, unload)


def test_balance_1():
    manifest = open("case1.txt", "r", encoding="ascii")
    ship_bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    for line in manifest:
        line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        data = line.split(",")
        if str(data[3].strip()) != "UNUSED":
            row = ship_bay.get_height() - int(data[0])
            col = int(data[1]) - 1
            cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
            ship_bay.add_container(cont, row, col)

    ship_bay.convert_grid_to_stack()
    buffer.convert_grid_to_stack()

    o = Optimizer.Optimizer()

    return o.balance(ship_bay, buffer)


def test_sift():
    manifest = open("case5.txt", "r", encoding="ascii")
    ship_bay = Grid.ShipBay()
    buffer = Grid.Buffer()
    for line in manifest:
        line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        data = line.split(",")
        if str(data[3].strip()) != "UNUSED":
            row = ship_bay.get_height() - int(data[0])
            col = int(data[1]) - 1
            cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
            ship_bay.add_container(cont, row, col)

    ship_bay.convert_grid_to_stack()
    buffer.convert_grid_to_stack()

    o = Optimizer.Optimizer()

    return o.balance(ship_bay, buffer)


# vals, n_expanded, max_n = test_load_unload()

# while vals is not None:
#     print(vals.get_bay())
#     vals = vals.get_parent_move()

# print("Expanded: %s" % n_expanded)
# print("Max: %s" % max_n)

vals, n_expanded, max_n = test_balance_1()

while vals is not None:
    print(vals.get_bay())
    vals = vals.get_parent_move()

print("Expanded: %s" % n_expanded)
print("Max: %s" % max_n)

# vals, n_expanded, max_n = test_sift()

# while vals is not None:
#     print(vals.get_bay())
#     vals = vals.get_parent_move()

# print("Expanded: %s" % n_expanded)
# print("Max: %s" % max_n)
