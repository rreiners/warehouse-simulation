from collections import deque


class Warehouse:
    def __init__(self, layout):
        self.layout = layout
        self.item_locations = {}
        self.start = None
        self.printer = None

    def set_start(self, start):
        self.start = start

    def set_printer(self, printer):
        self.printer = printer

    def add_item_location(self, item, location):
        self.item_locations[item] = location

    def find_path(self, start, end):
        # Directions represented as (row_change, column_change)
        directions = {
            ">": (0, 1),
            "<": (0, -1),
            "^": (-1, 0),
            "v": (1, 0),
            ">v": [(0, 1), (1, 0)],
            "<v": [(0, -1), (1, 0)],
            "^>": [(-1, 0), (0, 1)],
            "^<": [(-1, 0), (0, -1)],
            "v>": [(1, 0), (0, 1)],
            "v<": [(1, 0), (0, -1)],
            "<>": [(0, -1), (0, 1)],
            "^v": [(-1, 0), (1, 0)],
            # Add more combinations if needed
        }
        queue = deque([(start, [start])])

        while queue:
            current_position, path = queue.popleft()

            if current_position == end:
                return path  # Path found

            current_row, current_col = current_position
            cell_value = self.layout[current_row][current_col]
            if cell_value in directions:
                # Check if the path allows multiple directions
                next_steps = directions[cell_value]
                if isinstance(next_steps[0], tuple):
                    for step in next_steps:
                        self.add_to_queue(step, current_row, current_col, path, queue)
                else:
                    self.add_to_queue(next_steps, current_row, current_col, path, queue)

        return []  # No path found

    def add_to_queue(self, step, current_row, current_col, path, queue):
        delta_row, delta_col = step
        next_position = (current_row + delta_row, current_col + delta_col)

        # Check bounds and whether next cell is a wall or rack
        if (
            0 <= next_position[0] < len(self.layout)
            and 0 <= next_position[1] < len(self.layout[0])
            and self.layout[next_position[0]][next_position[1]] != "X"
        ):
            new_path = path + [next_position]
            queue.append((next_position, new_path))

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
        total_path = [self.start]
        distances = []
        current_position = self.start
        total_distance = 0

        for order in orders:
            item_location = self.item_locations.get(order)
            if item_location:
                item_path = self.find_path(current_position, item_location)
                if item_path:
                    # We subtract 1 to account for the overlap between paths
                    distance_to_item = len(item_path) - 1
                    total_distance += distance_to_item
                    distances.append(distance_to_item)
                    # Exclude the first element to avoid duplication
                    total_path.extend(item_path[1:])
                    current_position = item_location
                else:
                    raise ValueError(f"Path to item {order} not found")
            else:
                raise ValueError(f"Item {order} location not found")

        # Finally, path to the printer and its distance
        printer_path = self.find_path(current_position, self.printer)
        if printer_path:
            distance_to_printer = len(printer_path) - 1
            total_distance += distance_to_printer
            distances.append(distance_to_printer)
            total_path.extend(printer_path[1:])
        else:
            raise ValueError("Path to printer not found")

        return total_path, distances, total_distance


## Assuming your warehouse_layout is a 2D list with the correct symbols for direction
warehouse_layout = [
    [">v", ">", ">", ">v", ">", ">", ">", "v"],
    ["v", "X", "X", "v", "X", "X", "X", "v"],
    ["v", "<", "<", "<v", "<", "<", "<", "<v"],
    ["v", "X", "X", "v", "X", "X", "X", "v"],
    ["v>", ">", ">", "v>", ">", ">", ">", ">v"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
]

warehouse = Warehouse(warehouse_layout)
warehouse.set_start((0, 0))  # Set start location
warehouse.set_printer((4, 7))  # Set printer location row 4 column 7
# Define item locations
warehouse.add_item_location("Item1", (2, 2))
warehouse.add_item_location("Item2", (4, 5))

# ... Continue setting up items ...

# Simulate order
orders = ["Item1", "Item2"]  # List of items in the order
path, distances, total_distance = warehouse.simulate_order(orders)
print(path)
print(f"Path for order: {orders}")
print(f"Individual distances: {distances}")
print(f"Total distance traveled: {total_distance}")
