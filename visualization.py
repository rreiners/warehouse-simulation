import pygame
import time
import sys

from simulation import (
    Warehouse,
    warehouse_layout,
)  # Import ne

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

# Simulate order
orders = ["Item1", "Item2"]  # List of items in the order
path, distances, total_distance = warehouse.simulate_order(orders)
print(path)
print(f"Path for order: {orders}")
print(f"Individual distances: {distances}")
print(f"Total distance traveled: {total_distance}")

# Initialize pygame
pygame.init()

# Constants for the display
CELL_SIZE = 60
CELL_MARGIN = 2
WINDOW_WIDTH = len(warehouse_layout[0]) * (CELL_SIZE + CELL_MARGIN)
WINDOW_HEIGHT = len(warehouse_layout) * (CELL_SIZE + CELL_MARGIN)

# Colors
BACKGROUND_COLOR = pygame.Color("white")
RACK_COLOR = pygame.Color("grey")
PATH_COLOR = pygame.Color("lightblue")
START_COLOR = pygame.Color("green")
PRINTER_COLOR = pygame.Color("red")
ITEM_COLOR = pygame.Color("orange")
PICKER_COLOR = pygame.Color("blue")

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Warehouse Picker Simulation")


def draw_warehouse():
    for row_index, row in enumerate(warehouse_layout):
        for col_index, cell in enumerate(row):
            rect = pygame.Rect(
                col_index * (CELL_SIZE + CELL_MARGIN),
                row_index * (CELL_SIZE + CELL_MARGIN),
                CELL_SIZE,
                CELL_SIZE,
            )
            if cell == "X":
                color = RACK_COLOR
            elif cell in [
                ">",
                "<",
                "^",
                "v",
                ">v",
                "<v",
                "^>",
                "^<",
                "v>",
                "v<",
                "<>",
                "^v",
            ]:
                color = PATH_COLOR
            else:
                color = BACKGROUND_COLOR

            if (row_index, col_index) == warehouse.start:
                color = START_COLOR
            elif (row_index, col_index) == warehouse.printer:
                color = PRINTER_COLOR
            elif (row_index, col_index) in warehouse.item_locations.values():
                color = ITEM_COLOR
            pygame.draw.rect(screen, color, rect)


def draw_path(path):
    for position in path:
        row, col = position
        rect = pygame.Rect(
            col * (CELL_SIZE + CELL_MARGIN),
            row * (CELL_SIZE + CELL_MARGIN),
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, PICKER_COLOR, rect)
        pygame.display.flip()  # Update the display to show the new color
        if (row, col) == warehouse.printer:
            # sleep for a while and then quit the game
            time.sleep(2)
            pygame.quit()
        else:
            time.sleep(0.5)  # Wait half a second to visualize the movement


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    draw_warehouse()
    draw_path(path)  # `path` should be the path variable from your simulation

    pygame.display.flip()

# Quit pygame
pygame.quit()
