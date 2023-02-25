"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import container as Container


def get_child(state, task):
    """Gets the children of possible actions to take"""
    children = []
    if task == "loading":
        for i in range(0, 13):
            children.append(apply_operations(state, i))
    elif task == "balance":
        for i in range(0, 12):
            children.append(apply_operations(state, i))
    else:
        raise ValueError('Invalid task, must be "loading" or "balance"')

    return state


def apply_operations(container=Container.Container(), operation=0):
    """Updates a container's state given an operation"""
    return
