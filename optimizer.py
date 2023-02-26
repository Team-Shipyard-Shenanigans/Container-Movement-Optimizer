"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import container as Container


def onload(bay, container_onload_list, container_offload_list):
    return


def balance(bay):
    return


def get_child(bay, buffer, task):
    """Gets the children of possible actions to take"""
    children = []
    if task == "loading":
        children.append(apply_load_operations(bay, buffer, g))
    elif task == "balance":
        children.append(apply_balance_operations(bay, buffer,))
    else:
        raise ValueError('Invalid task, must be "loading" or "balance"')

    return bay


def get_containers(bay, buffer, container=Container.Container()):
    """Gets all target containers based on description"""
    container_array = []
    for i in bay:
        for j in i:
            if j.get_description() == container.get_description():
                container_array.append(j)
    return container_array


def apply_load_operations(bay, buffer, container_array):
    """Gets all target containers based on description"""

    return container_array


def apply_balance_operations(bay):
    return
