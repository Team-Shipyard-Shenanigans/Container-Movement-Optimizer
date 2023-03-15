"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import container as Container
import copy as copy


class Optimizer:
    def load(self, bay, container_onload_list, container_offload_list):
        nodes = [(bay, (-1, -1), True, 0)]
        path_tree = []
        repeated_states = []
        min_index = 0
        while len(nodes) > 0:
            curr = nodes.pop(min_index)  ## Remove the smallest cost node from the queue
            path_tree.append(curr)
            if curr[0].contains_all(container_offload_list) and ~curr[0].contains_any(container_onload_list):  ## If our popped node is our goal state, we've solved the puzzle!
                return path_tree, curr[0]  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            else:
                children = self.apply_load_operations(curr, container_offload_list, container_onload_list)
                for i in children:
                    if i not in repeated_states:
                        nodes.append(i)
                        repeated_states.append(i)
                ## Sort Queue based on our Heuristic
                min_node = (0, nodes[0])
                for i in enumerate(nodes):
                    if min_node[3] >= i[3]:
                        min_node = i
                min_index = min_node[0]
        return

    def balance(self):
        return

    def get_containers(self, bay, container=Container.Container()):
        """Gets all target containers based on description"""
        container_array = []
        for i in bay.get_grid():
            for j in i:
                if j is not None and j.get_description() == container.get_description():
                    container_array.append(j)
        return container_array

    def apply_load_operations(self, current_node, offload_list, onload_list):
        nodes = [()]
        curr_bay = current_node[0]
        curr_crane_pos = current_node[1]
        on_ship = current_node[2]
        prev_cost = current_node[3]
        if on_ship:
            for container in offload_list:
                origin_column = container.get_location(1)
                if container.is_on_ship():
                    bay_copy = copy.deepcopy(curr_bay)
                    stack_top = bay_copy.get_stacks(origin_column).pop()

                    if container is stack_top:
                        nodes.append((bay_copy, (-1, 23), ~on_ship, prev_cost + self.buffer_move_cost(container) + stack_top.get_cost(curr_crane_pos) - 1))
                    else:
                        for i in bay_copy.get_stacks():
                            dest_column = i.get_column()
                            dest_height = i.get_height()
                            if dest_column is not origin_column:
                                copy2 = copy.deepcopy(bay_copy)
                                new_crane_pos = (dest_height + 2, dest_column)
                                copy2.move_to_column(dest_column)
                                nodes.append((copy2, new_crane_pos, True, prev_cost + self.column_move_cost(copy2, origin_column, dest_column) + stack_top.get_cost(curr_crane_pos) - 1))
                    bay_copy.get_stacks(origin_column).append(stack_top)
        else:
            for container in onload_list:
                if not container.is_on_ship():
                    bay_copy = current_node[0]
                    for i in bay_copy.get_stacks():
                        dest_column = i.get_column()
                        dest_height = i.get_height()
                        copy2 = copy.deepcopy(bay_copy)
                        new_crane_pos = (dest_height + 2, dest_column)
                        cont_copy = copy.deepcopy(container)
                        cont_copy.move((i.get_height(), i.get_column()))
                        copy2.add_container(cont_copy)
                        nodes.append((copy2, new_crane_pos, True, prev_cost + self.buffer_move_cost(cont_copy)))
        return nodes

    def apply_balance_operations(self):
        pass

    def buffer_move_cost(self, container):
        return container.get_cost((-1, 0)) + 4 if container.is_on_ship() else container.get_cost((-1, 23)) + 4

    def column_move_cost(self, bay, origin_column, dest_column):
        origin_stack = bay.get_stacks(origin_column)

        origin_height = origin_stack.get_height()

        if origin_height == 0:
            raise ValueError("Cannot compute movement cost if origin stack is empty")

        dest_stack = bay.get_stacks(dest_column)
        dest_height = dest_stack.get_height()

        height = max(j.get_height() for j in bay.get_stacks()[min(dest_column, origin_column) : max(dest_column, origin_column)])
        dX = abs(dest_column - origin_column)
        dY = abs(height + 1 - origin_height) + abs(height - (dest_height + 1)) if origin_height < height else abs(dest_height + 1 - origin_height)
        return dX + dY
