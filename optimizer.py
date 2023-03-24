"""
Optimizer module contains functions relating to performing A* search on the ship grid given a task.
"""
import copy
import move


class Optimizer:
    def load(self, bay, buffer, container_onload_list, container_offload_list):
        nodes = [move.Move(bay, buffer, None, (-1, 0), container_offload_list, container_onload_list, True, 0, None, None, None)]
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

    def balance(self, bay, buffer):
        nodes = [move.Move(bay, buffer, None, (-1, 0), None, None, True, 0, None, None, None)]
        
        if(self.check_sift(nodes[0])):
            return self.sift(bay, buffer)
        
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
                    j = j[0]
                    origin_stack = curr_bay.get_stacks(j)
                    origin_max_height = origin_stack.get_max_height()
                    origin_height = origin_stack.get_height()
                    cont_pos = (origin_max_height - (origin_height + 1), j)
                    if origin_stack.peek().get_description() == i.get_description():
                        bay_copy = copy.deepcopy(curr_bay)
                        bay_copy.move_to_column(j, -1)
                        offload_remaining = copy.deepcopy(curr_move.get_offload_remaining())
                        offload_remaining.remove(i)
                        cost = prev_cost + bay_copy.manhattan(prev_pos, (cont_pos[0], cont_pos[1] + 1)) + curr_move.buffer_move_cost(cont_pos, True)
                        moves.append(move.Move(bay_copy, curr_buffer, prev_pos, (-1, 23), offload_remaining, curr_move.get_onload_remaining(), False, cost, curr_move, i, cont_pos))
                    else:
                        for i in curr_bay.get_stacks():
                            dest_col = i.get_column()
                            if dest_col != j:
                                bay_copy = copy.deepcopy(curr_bay)
                                cost = prev_cost + bay_copy.manhattan(prev_pos, cont_pos) + curr_move.column_move_cost(j, dest_col, on_ship)
                                ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                                bay_copy.move_to_column(j, dest_col)
                                dest_stack = bay_copy.get_stacks(dest_col)
                                moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, cost, curr_move, dest_stack.peek(), cont_pos))
                        for i in curr_buffer.get_stacks(): ## for all destination locations within the bay
                            dest_col = i.get_column()
                            dest_height = i.get_max_height() - (i.get_height() + 1)
                            if i.get_height() < i.get_max_height():
                                bay_copy = copy.deepcopy(curr_bay)
                                buffer_copy = copy.deepcopy(curr_buffer)
                                cost = prev_cost + curr_move.buffer_move_cost(prev_pos, False) + dest_col + abs(-1 - dest_height)
                                ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                                buffer_copy.move_to_column(-1, dest_col, origin_stack.peek())
                                bay_copy.move_to_column(j, -1, origin_stack.peek())
                                moves.append(move.Move(bay_copy, buffer_copy, prev_pos, ending_loc, curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, cost, curr_move, origin_stack.peek(), cont_pos))
            moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 23), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), False, prev_cost + curr_move.buffer_move_cost(curr_crane_pos, True), curr_move, None, None))
        else:
            moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 0), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, prev_cost + curr_move.buffer_move_cost(curr_crane_pos, True), curr_move, None, None))
            for i in curr_move.get_onload_remaining():
                for j in curr_bay.get_stacks():
                    if j.get_height() < j.get_max_height():
                        bay_copy = copy.deepcopy(curr_bay)
                        dest_col = j.get_column()
                        dest_height = j.get_max_height() - (j.get_height() + 1)
                        cost = prev_cost + curr_move.buffer_move_cost(curr_crane_pos, False) + dest_col + abs(-1 - dest_height)
                        ending_loc = (j.get_max_height() - (j.get_height() + 2), dest_col)
                        bay_copy.move_to_column(-1, dest_col, i)
                        onload_remaining = copy.deepcopy(curr_move.get_onload_remaining())
                        onload_remaining.remove(i)
                        moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), onload_remaining, True, cost, curr_move, i, None))
        return moves

    def apply_balance_operations(self, curr_move) -> list["move.Move"]:
        """Apply balance operations to the current move."""
        moves = []
        curr_bay = curr_move.get_bay()
        curr_buffer = curr_move.get_buffer()
        prev_pos = curr_move.get_end_pos()
        prev_cost = curr_move.get_cost()
        on_ship = curr_move.get_in_bay()

        for top in curr_move.get_top_containers():
            j = top[1]
            origin_stack = curr_bay.get_stacks(j) if on_ship else curr_buffer.get_stacks(j)
            origin_max_height = origin_stack.get_max_height()
            origin_height = origin_stack.get_height()
            cont_pos = (origin_max_height - (origin_height + 1), j)
            for i in curr_bay.get_stacks(): ## for all destination locations within the bay
                dest_col = i.get_column()
                dest_height = i.get_max_height() - (i.get_height() + 1)
                if on_ship:
                    if i.get_height() < curr_bay.get_rows() and dest_col != j:
                        bay_copy = copy.deepcopy(curr_bay)
                        cost = prev_cost + bay_copy.manhattan(prev_pos, cont_pos) + curr_move.column_move_cost(j, dest_col, on_ship)
                        ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                        bay_copy.move_to_column(j, dest_col)
                        moves.append(move.Move(bay_copy, curr_buffer, prev_pos, ending_loc, curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, cost, curr_move, origin_stack.peek(), cont_pos))
                else:
                    if i.get_height() < i.get_max_height():
                        bay_copy = copy.deepcopy(curr_bay)
                        buffer_copy = copy.deepcopy(curr_buffer)
                        cost = prev_cost + curr_move.buffer_move_cost(prev_pos, False) + dest_col + abs(-1 - dest_height)
                        ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                        bay_copy.move_to_column(-1, dest_col, i)
                        buffer_copy.move_to_column(j, -1, i)
                        moves.append(move.Move(bay_copy, buffer_copy, prev_pos, ending_loc, None, None, True, cost, curr_move, i, cont_pos))
            
            for i in curr_buffer.get_stacks(): ## for all destination locations within the bay
                dest_col = i.get_column()
                dest_height = i.get_max_height() - (i.get_height() + 1)
                if not on_ship:
                    if i.get_height() < i.get_max_height() and dest_col != j:
                        buffer_copy = copy.deepcopy(curr_buffer)
                        cost = prev_cost + buffer_copy.manhattan(prev_pos, cont_pos) + curr_move.column_move_cost(j, dest_col, on_ship)
                        ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                        buffer_copy.move_to_column(j, dest_col)
                        moves.append(move.Move(curr_bay, buffer_copy, prev_pos, ending_loc, None, None, True, cost, curr_move, origin_stack.peek(), cont_pos))
                else:
                    if i.get_height() < i.get_max_height():
                        bay_copy = copy.deepcopy(curr_bay)
                        buffer_copy = copy.deepcopy(curr_buffer)
                        cost = prev_cost + curr_move.buffer_move_cost(prev_pos, False) + dest_col + abs(-1 - dest_height)
                        ending_loc = (i.get_max_height() - (i.get_height() + 2), dest_col)
                        buffer_copy.move_to_column(-1, dest_col, origin_stack.peek())
                        bay_copy.move_to_column(j, -1, origin_stack.peek())
                        moves.append(move.Move(bay_copy, buffer_copy, prev_pos, ending_loc, None, None, True, cost, curr_move, origin_stack.peek(), cont_pos))
        if on_ship:
            moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 23), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), False, prev_cost + curr_move.buffer_move_cost(prev_pos, False), curr_move, None, None))
        else:
            moves.append(move.Move(curr_bay, curr_buffer, prev_pos, (-1, 0), curr_move.get_offload_remaining(), curr_move.get_onload_remaining(), True, prev_cost + curr_move.buffer_move_cost(prev_pos, True), curr_move, None, None))
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

    def get_min_move_col(self, j, curr_move, in_bay, no_transfer):
        grid = curr_move.get_bay() if in_bay else curr_move.get_buffer()
        min_cost = 100000
        min_col = j

        if no_transfer:
            for dest_col in range(0, j):
                cost = curr_move.column_move_cost(j, dest_col, in_bay)
                if cost < min_cost:
                    min_cost = cost
                    min_col = dest_col
            for dest_col in range(j + 1, grid.get_columns()):
                cost = curr_move.column_move_cost(j, dest_col, in_bay)
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
            j = target[1]
            stack = bay.get_stacks(j)
            temp = []
            while stack.peek() is not None and stack.peek() != target[0]:
                cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), j))
                prev_pos, min_cost = self.get_min_move_col(j, curr_move, True, True)
                cost += min_cost
                temp.append(stack.pop())
            cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), j)) + curr_move.column_move_cost(j, dest_side, True)

            for k in reversed(temp):
                stack.push(k)

            greater_mass -= target[0].get_weight()
            lesser_mass += target[0].get_weight()
            deficit -= target[0].get_weight()
            conts_to_move.remove(target)
        return cost

    def check_sift(self, move=move.Move):
        balanced, left_mass, right_mass = move.check_balanced()

        balanced_mass = (left_mass + right_mass) / 2

        for i in move.get_containers_in_section((0, move.get_bay().get_rows()), (0, move.get_bay().get_columns())):
            if i[0].get_weight() > balanced_mass:
                return True
        return False

    def sift(self, bay, buffer):
        nodes = [move.Move(bay, buffer, None, (-1, 0), None, None, True, 0, None, None, None)]
        
        min_index = 0
        nodes_expanded = 0
        max_nodes_in_queue = 0

        goal = self.generate_sift_goal(nodes[0])

        while len(nodes) > 0:
            nodes_expanded += 1
            max_nodes_in_queue = max(max_nodes_in_queue, len(nodes))
            curr = nodes.pop(min_index)  ## Remove the smallest cost node from the queue

            if self.sift_heuristic(curr, goal) == 0:  ## If our popped node is our goal state, we've solved the puzzle!
                return curr, nodes_expanded, max_nodes_in_queue  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
            children = self.apply_balance_operations(curr)
            for i in children:
                if i not in nodes:
                    nodes.append(i)
            ## Sort Queue based on our Heuristic
            min_node = (0, nodes[0])
            for i in enumerate(nodes):
                f_1 = self.sift_heuristic(min_node[1], goal) + min_node[1].get_cost()
                f_2 = self.sift_heuristic(i[1], goal) + i[1].get_cost()
                #print("Move %s To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (i[1].get_container(), i[1].get_end_pos(), i[1].get_init_pos(), i[1].get_in_bay(), f_2, f_2 - i[1].get_cost(), i[1].get_cost()))
                #print(i[1].get_bay())
                if f_1 >= f_2:
                    min_node = i
            min_index = min_node[0]
            #print("Choosing: Move %s To %s From %s End in Bay? %s, F(N) = %s, H(N) = %s, G(N) = %s" % (min_node[1].get_container(), min_node[1].get_end_pos(), min_node[1].get_init_pos(), min_node[1].get_in_bay(), f_1, f_1 - min_node[1].get_cost(), min_node[1].get_cost()))

    def sift_heuristic(self, curr_move, goal_state):
        bay = curr_move.get_bay()
        grid = curr_move.get_bay().get_grid()
        cost = 0
        mismatch = []
        prev_pos = curr_move.get_end_pos()

        for i in range(curr_move.get_bay().get_rows()):
            for j in range(curr_move.get_bay().get_columns()):
                if grid[i][j] != goal_state[i][j] and grid[i][j] is not None and grid[i][j].get_description() != "NAN":
                    mismatch.append((grid[i][j]))
        
        
        for stack in bay.get_stacks():
            temp = []
            # print(stack)
            # print(cost)
            while stack.peek() is not None and stack.has(mismatch):
                goal_indices = self.get_sift_goal_loc(curr_move, (stack.peek(), stack.get_column()))   
                cost += bay.manhattan(prev_pos, (stack.get_max_height() - (stack.get_height() + 1), stack.get_column()))
                dest_stack = bay.get_stacks(goal_indices[1])
                dest_row = dest_stack.get_max_height() - (dest_stack.get_height() + 1)
                min_cost = curr_move.column_move_cost(stack.get_column(), goal_indices[1], True) + abs(goal_indices[0] - dest_row) 
                prev_pos = (dest_row, goal_indices[1])
                cost += min_cost
                temp.append(stack.pop())      
            for k in reversed(temp):
                stack.push(k)
        
        return cost
    
    def get_sift_goal_loc(self, curr_move, container):
        containers = curr_move.get_containers_in_section((0, curr_move.get_bay().get_rows()), (0, curr_move.get_bay().get_columns()))
        containers.sort(key=lambda x: x[0].get_weight(), reverse=True)
        return self.index_mapper(containers.index(container))

    def index_mapper(self, index):
        return (7 - int(index / 12), index % 12)

    def generate_sift_goal(self, curr_move):
        rows = curr_move.get_bay().get_rows()
        cols = curr_move.get_bay().get_columns()
        goal = [[None] * cols for i in range(rows)]

        for i in range(rows):
            for j in range(cols):
                if(curr_move.get_bay().get_container(i, j) is not None and curr_move.get_bay().get_container(i, j).get_description() == "NAN"):
                    goal[i][j] = curr_move.get_bay().get_grid()[i][j]

        containers = curr_move.get_containers_in_section((0, rows), (0, cols))
        containers.sort(key=lambda x: x[0].get_weight(), reverse=True)
        
        index_adjustment = 0
        for i in enumerate(containers):
            goal_loc = self.index_mapper(i[0] + index_adjustment)
            if (goal[goal_loc[0]][goal_loc[1]] is None):
                goal[goal_loc[0]][goal_loc[1]] = i[1][0]
            else:
                while(goal[goal_loc[0]][goal_loc[1]] is not None):
                    index_adjustment += 1
                    goal_loc = self.index_mapper(i[0] + index_adjustment)
                goal[goal_loc[0]][goal_loc[1]] = i[1][0]

        return goal
