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

        while len(nodes) > 0:
            curr = nodes.pop(0)  ## Remove the smallest cost node from the queue
            if curr[0].contains_all(container_offload_list) and ~curr[0].contains_any(container_onload_list):  ## If our popped node is our goal state, we've solved the puzzle!
                print("Goal State found!")
                return nodes, curr[1]  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            else:
                nodes.append(self.apply_load_operations(container_offload_list))
                ## Sort Queue based on our Heuristic
        return

    def balance(self):
        return

    def get_containers(self, container=Container.Container()):
        """Gets all target containers based on description"""
        container_array = []
        for i in self.bay:
            for j in i:
                if j.get_description() == container.get_description():
                    container_array.append(j)
        return container_array

    def apply_load_operations(self, container_array):
        animations = []
        for container in container_array:
            if container.is_on_ship():
                buffer_cost = self.buffer_move_cost(container)
                column_cost, column, height = self.column_move_cost(container.get_location()[1])
                animation = self.move_to_column(container, column, height) if buffer_cost >= column_cost else self.move_to_buffer(container)
                animations.append(animation)

        return container_array

    def move_to_column(self, container, column, dest_height):
        animation = []
        origin_column = container.get_location[1]
        origin_stack = self.bay.get_stacks(origin_column)
        origin_height = 8 - self.bay.get_stacks()[container.get_location()[0]]
        container_height = origin_stack.get_height()

        dest_stack = self.bay.get_stacks(column)

        for i in range(origin_height, dest_height):
            animation.append((container_height, 8 - i))
        for i in range(origin_column, column):
            animation.append((dest_height, i))

        dest_stack.push(origin_stack.pop())

        return

    def move_to_buffer(self, container):
        animation = []
        origin_column = container.get_location[1]
        origin_stack = self.bay.get_stacks(origin_column)
        origin_height = 8 - self.bay.get_stacks()[container.get_location()[0]]
        container_height = origin_stack.get_height()

        for i in range(origin_height, 8):
            animation.append((container_height, 8 - i))
        for i in range(origin_column, 0):
            animation.append((0, i))

        return animation

    def buffer_move_cost(self, container):
        return container.get_cost((-1, 0)) + 4 if container.is_on_ship() else container.get_cost((-1, 23)) + 4

    def column_move_cost(self, column):
        stack = self.bay.get_stacks()[column]
        min_cost = (stack, 1000000)
        height = 10000
        for i in self.bay.get_stacks():
            if i.get_column() != column:
                if i.get_height() <= 7:
                    temp_cost = abs(i.get_column() - column) + abs(height - stack.height()) + abs(height - i.height())
                    min_cost = (i, temp_cost) if min_cost[1] >= temp_cost else min_cost
        return min_cost[1], min_cost[0].get_column(), height
