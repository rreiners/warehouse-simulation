import heapq
from itertools import combinations, permutations
from collections import deque


class Warehouse:
    def __init__(self, layout):
        self.layout = layout
        self.item_locations = {}
        self.start = None
        self.printer = None
        self.path_cache = {}  # Hinzugefügt für das Caching von Pfaden

    def set_start(self, start):
        self.start = start

    def set_printer(self, printer):
        self.printer = printer

    def add_item_location(self, item, location):
        self.item_locations[item] = location

    def manhattan_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # Function to generate all combinations of directions
    def generate_direction_permutations(self, basic_directions):
        keys = list(basic_directions.keys())
        directions_dict = {}

        # Generate all non-empty subsets of the basic directions
        for r in range(1, len(keys) + 1):
            for combo in combinations(keys, r):
                # Generate all permutations for each combination
                for perm in permutations(combo):
                    perm_key = "".join(perm)
                    # Map each permutation to its corresponding movement deltas
                    if (
                        perm_key not in directions_dict
                    ):  # Check to avoid duplicate entries
                        directions_dict[perm_key] = [
                            basic_directions[direction] for direction in perm
                        ]

        return directions_dict

    def find_path(self, start, end):
        if (start, end) in self.path_cache:
            return self.path_cache[(start, end)]

        # Open set as a heap queue
        open_set = []
        heapq.heappush(
            open_set, (0 + self.manhattan_distance(start, end), 0, start, [start])
        )

        basic_directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

        directions = self.generate_direction_permutations(basic_directions)

        while open_set:
            _, cost, current_position, path = heapq.heappop(open_set)

            if current_position == end:
                self.path_cache[(start, end)] = path
                return path

            current_row, current_col = current_position
            cell_value = self.layout[current_row][current_col]
            if cell_value in directions:
                next_steps = directions[cell_value]
                if isinstance(next_steps[0], tuple):
                    for step in next_steps:
                        self._add_to_queue(
                            step, cost, current_row, current_col, path, open_set, end
                        )
                else:
                    self._add_to_queue(
                        next_steps, cost, current_row, current_col, path, open_set, end
                    )

        return []

    def _add_to_queue(self, step, cost, current_row, current_col, path, open_set, end):
        delta_row, delta_col = step
        next_position = (current_row + delta_row, current_col + delta_col)

        if (
            0 <= next_position[0] < len(self.layout)
            and 0 <= next_position[1] < len(self.layout[0])
            and self.layout[next_position[0]][next_position[1]] != "X"
            and next_position not in path
        ):
            new_path = path + [next_position]
            new_cost = cost + 1
            heapq.heappush(
                open_set,
                (
                    new_cost + self.manhattan_distance(next_position, end),
                    new_cost,
                    next_position,
                    new_path,
                ),
            )

    def get_path(self, orders):
        if not self.start or not self.printer:
            raise ValueError("Start or printer location not set")

        path = [self.start]
        current_position = self.start
        for order in orders:
            item_location = self.item_locations.get(order)
            if item_location:
                new_path = self.find_path(current_position, item_location)
                if new_path:
                    # Exclude the first element to avoid duplication
                    path.extend(new_path[1:])
                    current_position = item_location
                else:
                    raise ValueError(f"Path to item {order} not found")
            else:
                raise ValueError(f"Item {order} location not found")

        # Path to the printer
        new_path = self.find_path(current_position, self.printer)
        if new_path:
            path.extend(new_path[1:])
        else:
            raise ValueError("Path to printer not found")

        return path

    def simulate_order(self, orders):
        if not self.start or not self.printer:
            raise ValueError("Start or printer location not set")

        total_path = [self.start]
        distances = []
        current_position = self.start
        total_distance = 0

        for order in orders:
            item_location = self.item_locations.get(order)
            if item_location:
                item_path = self.find_path(current_position, item_location)
                if item_path:
                    distance_to_item = len(item_path) - 1
                    total_distance += distance_to_item
                    distances.append(distance_to_item)
                    total_path.extend(item_path[1:])
                    current_position = item_location
                else:
                    raise ValueError(f"Path to item {order} not found")
            else:
                raise ValueError(f"Item {order} location not found")

        printer_path = self.find_path(current_position, self.printer)
        if printer_path:
            distance_to_printer = len(printer_path) - 1
            total_distance += distance_to_printer
            distances.append(distance_to_printer)
            total_path.extend(printer_path[1:])
        else:
            raise ValueError("Path to printer not found")

        return total_path, distances, total_distance

if __name__ == "__main__":
        
    warehouse_layout = [
        ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
        [">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">v", ">v", ">v"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "<v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "<", "<", "<", "<"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "<v", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<", "<v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "v", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "v", "X", "X", "X", "X"],
        ["^v>", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", ">v", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">v", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X","X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ]


    warehouse = Warehouse(warehouse_layout)
    warehouse.set_start((20, 0))  # Set start location
    warehouse.set_printer((21, 0))  # Set printer/end location row 21 column 0
    # Define item locations
    warehouse.add_item_location("Item1", (1, 3))
    warehouse.add_item_location("Item2", (7, 13))

    # Simulate order
    orders = ["Item1", "Item2"]  # List of items in the order
    path, distances, total_distance = warehouse.simulate_order(orders)
    print(path)
    print(f"Path for order: {orders}")
    print(f"Individual distances: {distances}")
    print(f"Total distance traveled: {total_distance}")