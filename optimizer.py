## Helper function to get the child state given preset operators
def get_child(state, task):
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


def apply_operations(container, operation):
    return
