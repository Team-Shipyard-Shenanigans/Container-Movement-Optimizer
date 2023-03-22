"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import copy
import move


class Optimizer:
    def load(self, bay, buffer, container_onload_list, container_offload_list):
        nodes = [move.Move(bay, buffer, None, (-1, 0), container_offload_list, container_onload_list, True, 0, None, None)]
        bay_animation = []
        buffer_animation = []
        min_index = 0
        nodes_expanded = 0
        max_nodes_in_queue = 0
        while len(nodes) > 0:
            nodes_expanded += 1
            max_nodes_in_queue = max(max_nodes_in_queue, len(nodes))
            curr = nodes.pop(min_index)  ## Remove the smallest cost node from the queue
            # path_tree.append(curr)
            if len(curr.get_offload_remaining()) == 0 and len(curr.get_onload_remaining()) == 0:  ## If our popped node is our goal state, we've solved the puzzle!
                return curr, nodes_expanded, max_nodes_in_queue  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            children = self.apply_load_operations(curr)
            for i in children:
                if i not in nodes:
                    nodes.append(i)
            ## Sort Queue based on our Heuristic
            min_node = (0, nodes[0])
            for i in enumerate(nodes):
                f_1 = self.load_heuristic(min_node[1]) + min_node[1].get_cost()
                f_2 = self.load_heuristic(i[1]) + i[1].get_cost()
                # print("Move To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (i[1].get_end_pos(), i[1].get_init_pos(), i[1].get_in_bay(), f_2, f_2 - i[1].get_cost(), i[1].get_cost()))
                if f_1 >= f_2:
                    min_node = i
            min_index = min_node[0]
            # print("Choosing: Move To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (min_node[1].get_end_pos(), min_node[1].get_init_pos(), min_node[1].get_in_bay(), f_1, f_1 - min_node[1].get_cost(), min_node[1].get_cost()))
        return bay_animation, buffer_animation

    def balance(self, bay, buffer):
        nodes = [move.Move(bay, buffer, None, (-1, 0), None, None, True, 0, None, None)]
        min_index = 0
        nodes_expanded = 0
        max_nodes_in_queue = 0
        while len(nodes) > 0:
            nodes_expanded += 1
            max_nodes_in_queue = max(max_nodes_in_queue, len(nodes))
            curr = nodes.pop(min_index)  ## Remove the smallest cost node from the queue

            if curr.check_balanced()[0]:  ## If our popped node is our goal state, we've solved the puzzle!
                return curr, nodes_expanded, max_nodes_in_queue  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            children = self.apply_balance_operations(curr)
            for i in children:
                if i not in nodes:
                    nodes.append(i)
            ## Sort Queue based on our Heuristic
            min_node = (0, nodes[0])
            for i in enumerate(nodes):
                f_1 = self.balance_heuristic(min_node[1]) + min_node[1].get_cost()
                f_2 = self.balance_heuristic(i[1]) + i[1].get_cost()
                # print("Move %s To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (i[1].get_container(), i[1].get_end_pos(), i[1].get_init_pos(), i[1].get_in_bay(), f_2, f_2 - i[1].get_cost(), i[1].get_cost()))
                if f_1 >= f_2:
                    min_node = i
            min_index = min_node[0]
            # print("Choosing: Move %s To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (min_node[1].get_container(), min_node[1].get_end_pos(), min_node[1].get_init_pos(), min_node[1].get_in_bay(), f_1, f_1 - min_node[1].get_cost(), min_node[1].get_cost()))

    def apply_load_operations(self, curr_move):
        moves = []
        curr_bay = curr_move.get_bay()
        curr_buffer = curr_move.get_buffer()
        curr_crane_pos = curr_move.get_end_pos()
        on_ship = curr_move.get_in_bay()
        prev_cost = curr_move.get_cost()
        prev_pos = curr_move.get_end_pos()

        if on_ship:
            for i in curr_move.get_offload_remaining():
                for j in curr_bay.get_containers(i):
                    origin_col = j[0]
                    origin_stack = curr_bay.get_stacks(origin_col)
                    origin_max_height = origin_stack.get_max_height()
                    origin_height = origin_stack.get_height()
                    cont_pos = (origin_max_height - (origin_height + 1), origin_col)
                    if origin_stack.peek().get_description() == i.get_description():
                        bay_copy = copy.deepcopy(curr_bay)
                        bay_copy.move_to_column(origin_col, -1)
                        offload_remaining = copy.deepcopy(curr_move.get_offload_remaining())
                        offload_remaining.remove(i)
                        cost = prev_cost + bay_copy.manhattan(prev_pos, (cont_pos[0], cont_pos[1] + 1)) + curr_move.buffer_move_cost(cont_pos, True)
                        moves.append(move.Move(bay_copy, curr_buffer, prev_pos, (-1, 23), offload_remaining, curr_move.get_onload_remaining(), False, cost, curr_move, i))
                    else:
                        for i in curr_bay.get_stacks():
                            dest_col = i.get_column()
                            if dest_col != origin_col:
                                bay_copy = copy.deepcopy(curr_bay)
                                cost = prev_cost + bay_copy.manhattan(prev_pos, cont_pos) + curr_move.column_move_cost(origin_col, dest_col)
                                ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                                bay_copy.move_to_column(origin_col, dest_col)
                                moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, cost, curr_move, i.peek()))
            if len(curr_move.get_onload_remaining()) > 0:
                moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 23), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), False, prev_cost + curr_move.buffer_move_cost(curr_crane_pos, True), curr_move, None))
        else:
            moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 0), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, prev_cost + curr_move.buffer_move_cost(curr_crane_pos, True), curr_move, None))
            for i in curr_move.get_onload_remaining():
                for j in curr_bay.get_stacks():
                    if j.get_height() < j.get_max_height():
                        bay_copy = copy.deepcopy(curr_bay)
                        dest_col = j.get_column()
                        dest_height = j.get_max_height() - (j.get_height() + 1)
                        cost = prev_cost + curr_move.buffer_move_cost(curr_crane_pos, False) + dest_col + abs(-1 - dest_height)
                        ending_loc = (j.get_max_height() - (j.get_height() + 2), dest_col)
                        bay_copy.move_to_column(-1, dest_col, True, i)
                        onload_remaining = copy.deepcopy(curr_move.get_onload_remaining())
                        onload_remaining.remove(i)
                        moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), onload_remaining, True, cost, curr_move, i))
        return moves

    def apply_balance_operations(self, curr_move) -> list["move.Move"]:
        """Apply balance operations to the current move."""
        moves = []
        curr_bay = curr_move.get_bay()
        curr_buffer = curr_move.get_buffer()
        prev_pos = curr_move.get_end_pos()
        prev_cost = curr_move.get_cost()
        for top in curr_move.get_top_containers():
            origin_col = top[1]
            origin_stack = curr_bay.get_stacks(origin_col)
            origin_max_height = origin_stack.get_max_height()
            origin_height = origin_stack.get_height()
            cont_pos = (origin_max_height - (origin_height + 1), origin_col)
            for i in curr_bay.get_stacks():
                dest_col = i.get_column()
                if origin_stack.get_height() > 0 and i.get_height() < 8 and dest_col != origin_col:
                    bay_copy = copy.deepcopy(curr_bay)
                    cost = prev_cost + bay_copy.manhattan(prev_pos, cont_pos) + curr_move.column_move_cost(origin_col, dest_col)
                    ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                    bay_copy.move_to_column(origin_col, dest_col)
                    moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, cost, curr_move, origin_stack.peek()))

        return moves

    def load_heuristic(self, curr_move):
        cost = 0
        bay = curr_move.get_bay()
        onload_remaining = curr_move.get_onload_remaining()
        offload_remaining = curr_move.get_offload_remaining()
        prev_pos = curr_move.get_end_pos()
        num_offloads = len(offload_remaining)
        num_onloads = len(onload_remaining)
        for i in offload_remaining:
            for j in bay.get_containers(i):
                origin_col = j[0]
                stack = bay.get_stacks(origin_col)
                temp = []
                while stack.peek() is not None and stack.peek() != i:
                    cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), origin_col))
                    prev_pos, min_cost = self.get_min_move_col(origin_col, curr_move, True, True)
                    cost += min_cost
                    temp.append(stack.pop())
                cost += curr_move.buffer_move_cost((stack.get_max_height() - (stack.get_height() + 1), origin_col), True)

                cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), origin_col))
                for k in reversed(temp):
                    stack.push(k)

            if num_offloads - 1 > 0:  ## if there are more offloads to do we need to move the crane back from the buffer, we will also do onloads at this time
                cost += 4
            num_offloads -= 1
            num_onloads -= 1

        for i in range(0, num_onloads):
            pos, min_cost = self.get_min_move_col(0, curr_move, True, False)
            cost += 4 + min_cost
            if i < num_onloads - 1:
                cost += 4

        return cost

    def get_min_move_col(self, origin_col, curr_move, in_bay, no_transfer):
        grid = curr_move.get_bay() if in_bay else curr_move.get_buffer()
        min_cost = 100000
        min_col = origin_col
        if no_transfer:
            for dest_col in range(0, origin_col):
                cost = curr_move.column_move_cost(origin_col, dest_col)
                if cost < min_cost:
                    min_cost = cost
                    min_col = dest_col
            for dest_col in range(origin_col + 1, grid.get_columns()):
                cost = curr_move.column_move_cost(origin_col, dest_col)
                if cost < min_cost:
                    min_cost = cost
                    min_col = dest_col
        else:
            for j in grid.get_stacks():
                dest_col = j.get_column()
                cost = curr_move.buffer_move_cost((j.get_max_height() - (j.get_height() + 1), dest_col), True)
                if cost < min_cost:
                    min_cost = cost
                    min_col = dest_col

        min_stack = grid.get_stacks(min_col)
        dest_row = min_stack.get_max_height() - (min_stack.get_height() + 2)
        return (dest_row, min_col), min_cost

    def balance_heuristic(self, curr_move):
        balanced, left_mass, right_mass = curr_move.check_balanced()
        balanced_mass = (left_mass + right_mass) / 2

        bay = curr_move.get_bay()
        prev_pos = curr_move.get_end_pos()
        cost = 0

        lesser_mass = min(left_mass, right_mass)
        greater_mass = max(left_mass, right_mass)
        dest_side = 5 if left_mass >= right_mass else 6
        balanced_mass = (lesser_mass + greater_mass) / 2

        deficit = balanced_mass - lesser_mass

        row_int = (0, 8)
        col_int = (0, 6) if left_mass >= right_mass else (6, 12)

        conts_to_move = curr_move.get_containers_in_section(row_int, col_int)
        conts_to_move.sort(key=lambda x: x[0].get_weight(), reverse=False)
        # print("Lesser Mass %s, Greater Mass %s" % (lesser_mass, greater_mass))
        while lesser_mass / greater_mass < 0.9:
            target = None
            for i in conts_to_move:
                if i[0].get_weight() <= deficit:
                    target = i
            if target is None:
                break
            origin_col = target[1]
            stack = bay.get_stacks(origin_col)
            temp = []
            while stack.peek() is not None and stack.peek() != target[0]:
                cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), origin_col))
                prev_pos, min_cost = self.get_min_move_col(origin_col, curr_move, True, True)
                cost += min_cost
                temp.append(stack.pop())
            cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), origin_col)) + curr_move.column_move_cost(origin_col, dest_side)

            for k in reversed(temp):
                stack.push(k)

            greater_mass -= target[0].get_weight()
            lesser_mass += target[0].get_weight()
            deficit -= target[0].get_weight()
            conts_to_move.remove(target)
        return cost

    def sift(self, bay, buffer):
        pass

    def sift_heuristic(self, curr_move):
        pass
