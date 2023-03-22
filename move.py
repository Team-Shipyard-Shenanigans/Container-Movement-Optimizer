import copy
import grid as Grid
import container


class Move:
    def __init__(self, bay, buffer, crane_pos_initial, crane_pos_ending, offload_remaining, onload_remaining, end_in_bay, cost, parent_move, container):
        self.bay = bay
        self.buffer = buffer
        self.init_pos = crane_pos_initial
        self.end_pos = crane_pos_ending
        self.offload_remaining = offload_remaining
        self.onload_remaining = onload_remaining
        self.parent_move = parent_move
        self.cost = cost
        self.end_in_bay = end_in_bay
        self.container = container

    def get_bay(self) -> Grid.ShipBay:
        return self.bay

    def get_buffer(self) -> Grid.Buffer:
        return self.buffer

    def get_init_pos(self) -> tuple:
        return self.init_pos

    def get_end_pos(self) -> tuple:
        return self.end_pos

    def get_offload_remaining(self) -> list:
        return self.offload_remaining

    def get_onload_remaining(self) -> list:
        return self.onload_remaining

    def get_parent_move(self) -> "Move":
        return self.parent_move

    def get_in_bay(self) -> bool:
        return self.end_in_bay

    def get_cost(self) -> int:
        return self.cost

    def get_container(self) -> container.Container:
        return self.container

    def get_containers_in_section(self, row_int, col_int):
        containers = []
        for i in range(row_int[0], row_int[1]):
            for j in range(col_int[0], col_int[1]):
                cont = self.bay.get_container(i, j)
                if cont is not None:
                    containers.append((cont, j))
        return containers

    def buffer_move_cost(self, container_pos, crane_end_in_buffer) -> int:
        cont_grab_row = container_pos[0]
        cont_col = container_pos[1]
        crane_col = self.end_pos[1]
        crane_row = self.end_pos[0]
        base_cost = abs(cont_grab_row - crane_row) + abs(cont_col - crane_col)
        crane_end_row = -1
        crane_end_col = 0 if crane_end_in_buffer else 23

        return base_cost + abs(cont_grab_row - crane_end_row) + abs(cont_col - crane_end_col) + 4

    def column_move_cost(self, origin_column, dest_column) -> int:
        origin_stack = self.bay.get_stacks(origin_column)

        origin_height = origin_stack.get_height()

        if origin_height == 0:
            raise ValueError("Cannot compute movement cost if origin stack is empty")

        dest_stack = self.bay.get_stacks(dest_column)
        dest_height = dest_stack.get_height()
        if dest_height >= 8:
            return float("inf")

        if dest_column == origin_column:
            return 0

        height = max(j.get_height() for j in self.bay.get_stacks()[min(dest_column, origin_column) : max(dest_column, origin_column)])
        dX = abs(dest_column - origin_column)
        dY = abs(height + 1 - origin_height) + abs(height + 1 - (dest_height + 1)) if origin_height <= height else abs(dest_height + 1 - origin_height)
        return dX + dY

    def check_balanced(self):
        left_mass = 0
        right_mass = 0
        for i in range(0, 8):
            for j in range(0, 12):
                cont = self.get_bay().get_container(i, j)
                if cont is not None:
                    if int(j / 6) % 2 == 0:
                        left_mass += cont.get_weight()
                    else:
                        right_mass += cont.get_weight()
        return (min(left_mass, right_mass) / max(left_mass, right_mass)) >= 0.9, left_mass, right_mass

    def get_top_containers(self) -> list["container.Container"]:
        return [(i.peek(), i.get_column()) for i in self.bay.get_stacks()]

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Move) and self.bay == __o.bay and self.buffer == __o.buffer and self.init_pos == __o.init_pos and self.end_pos == __o.end_pos and self.end_in_bay == __o.end_in_bay

    def __hash__(self) -> int:
        return hash(self.end_pos, self.init_pos)
