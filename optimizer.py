"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import container as Container


class Optimizer:
    bay = []
    buffer = []

    def __init__(self, bay, buffer):
        self.bay = bay
        self.buffer = buffer

    def load(self, container_onload_list, container_offload_list):
        nodes = [(self.bay, 0)]
        path_tree = []
        while len(nodes) > 0:
            curr = nodes.pop(0)  ## Remove the smallest cost node from the queue
            path_tree.append(curr)
            if curr[0].contains_all(container_offload_list) and ~curr[0].contains_any(container_onload_list):  ## If our popped node is our goal state, we've solved the puzzle!
                print("Goal State found!")
                return nodes, curr[1]  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            else:
                children, animations = self.apply_load_operations(container_offload_list)
                for i in children:
                    nodes.append(i)
                ## Sort Queue based on our Heuristic
        return

    def balance(self):
        return

    def get_containers(self, container=Container.Container()):
        """Gets all target containers based on description"""
        container_array = []
        for i in self.bay.get_grid():
            for j in i:
                if j is not None and j.get_description() == container.get_description():
                    container_array.append(j)
        return container_array

    def apply_load_operations(self, container_array):
        for container in container_array:
            if container.is_on_ship():
                buffer_cost = self.buffer_move_cost(container)
                column_cost, column, height = self.column_move_cost(container.get_location()[1])
                self.move_to_column(container, column) if buffer_cost >= column_cost else self.move_to_buffer(container)

        return container_array

    def move_to_column(self, origin_column, dest_column):
        origin_stack = self.bay.get_stacks(origin_column)
        dest_stack = self.bay.get_stacks(dest_column)
        dest_stack.push(origin_stack.pop())

        return origin_stack, dest_stack

    def move_to_buffer(self, column):
        pass

    def buffer_move_cost(self, container):
        return container.get_cost((-1, 0)) + 4 if container.is_on_ship() else container.get_cost((-1, 23)) + 4

    def column_move_cost(self, origin_column):
        stack = self.bay.get_stacks(origin_column)

        if stack.get_height() == 0:
            raise ValueError("Cannot compute movement cost if origin stack is empty")

        min_cost = [100000, stack, stack.get_height()]

        for i in self.bay.get_stacks():
            dest_column = i.get_column()
            dest_height = i.get_height()
            if dest_column != origin_column:
                if i.get_height() <= 7:
                    height = dest_height
                    if abs(dest_column - origin_column) > 1:
                        height = max(j.get_height() for j in self.bay.get_stacks()[min(dest_column, origin_column) + 1 : max(dest_column, origin_column) - 1])
                    temp_cost = abs(dest_column - origin_column) + abs(height - stack.get_height() - 1) + abs(height - dest_height)
                    min_cost = (temp_cost, i, height) if min_cost[0] >= temp_cost else min_cost
        return min_cost
