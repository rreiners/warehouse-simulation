import pygame
import time
import sys
import csv

from simulation import Warehouse

warehouse_layout = []

# Open the CSV file and read the contents into the warehouse_layout list
with open("warehouse_layout.csv", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # Here we assume that your CSV file has each cell separated by commas,
        # and each row is a new line in the CSV
        warehouse_layout.append(row)

warehouse = Warehouse(warehouse_layout)
warehouse.set_start((20, 0))  # Set start location
warehouse.set_printer((21, 0))  # Set printer/end location row 21 column 0
# Define item locations
warehouse.add_item_location("Item1", (7, 13))
warehouse.add_item_location("Item2", (1, 3))
warehouse.add_item_location("Item3", (28, 18))

# Simulate order
orders = ["Item1", "Item2", "Item3"]  # List of items in the order
path, distances, total_distance = warehouse.simulate_order(orders)
print(f"Path for order: {orders}")
print(f"Individual distances: {distances}")
print(f"Total distance traveled: {total_distance}")

# Initialize pygame
pygame.init()

pygame.font.init()  # Initialize the font module
font = pygame.font.Font(None, 24)  # Choose the default font and set the size
# Constants for the display
CELL_SIZE = 10
CELL_MARGIN = 2
WINDOW_WIDTH = len(warehouse.layout[0]) * (CELL_SIZE + CELL_MARGIN)
WINDOW_HEIGHT = len(warehouse.layout) * (CELL_SIZE + CELL_MARGIN)

# Colors
BACKGROUND_COLOR = pygame.Color("white")
RACK_COLOR = pygame.Color("grey")
PATH_COLOR = pygame.Color("lightblue")
START_COLOR = pygame.Color("green")
PRINTER_COLOR = pygame.Color("red")
ITEM_COLOR = pygame.Color("orange")
PICKER_COLOR = pygame.Color("blue")

direction_symbols = {
    ">": ">",
    "<": "<",
    "^": "^",
    "v": "v",
    ">v": "",
    "<v": "↙",
    "^>": "↗",
    "^<": "↖",
    "v>": "↘",
    "v<": "↙",
    "<>": "↔",
    "^v": "↕",
    "^v<>": "✢",
    # ... add more mappings for other combinations as needed ...
}

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Warehouse Picker Simulation")


def draw_warehouse():
    for row_index, row in enumerate(warehouse.layout):
        for col_index, cell in enumerate(row):
            x = col_index * (CELL_SIZE + CELL_MARGIN)
            y = row_index * (CELL_SIZE + CELL_MARGIN)
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Determine the color based on the cell type
            if cell == "X":
                color = RACK_COLOR
            elif cell in direction_symbols.keys():
                color = PATH_COLOR
            else:
                color = BACKGROUND_COLOR

            # Draw the cell
            pygame.draw.rect(screen, color, rect)

            # Draw the direction symbol
            if cell in warehouse.generate_direction_permutations(
                {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
            ):
                # Use a larger font size if needed
                font = pygame.font.Font(None, CELL_SIZE)
                text_surface = font.render(cell, True, pygame.Color("black"))
                # Center the text
                screen.blit(text_surface, text_surface.get_rect(center=rect.center))

            # Highlight start, printer, and item locations
            if (row_index, col_index) == warehouse.start:
                color = START_COLOR
                pygame.draw.rect(screen, color, rect)
            elif (row_index, col_index) == warehouse.printer:
                color = PRINTER_COLOR
                pygame.draw.rect(screen, color, rect)
            elif (row_index, col_index) in warehouse.item_locations.values():
                color = ITEM_COLOR
                pygame.draw.rect(screen, color, rect)


def draw_path(path):
    for index, position in enumerate(
        path
    ):  # Enumerate to get both the index and the position

        row, col = position
        rect = pygame.Rect(
            col * (CELL_SIZE + CELL_MARGIN),
            row * (CELL_SIZE + CELL_MARGIN),
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, PICKER_COLOR, rect)
        pygame.display.flip()  # Update the display to show the new color
        if index == len(path) - 1:
            # Render and display distances after reaching the printer
            distances_text = f"Individual distances: {distances}"
            total_distance_text = f"Total distance traveled: {total_distance}"

            distances_surface = font.render(distances_text, True, pygame.Color("black"))
            total_distance_surface = font.render(
                total_distance_text, True, pygame.Color("black")
            )

            screen.blit(
                distances_surface, (50, WINDOW_HEIGHT - 50)
            )  # Adjust position as needed
            screen.blit(
                total_distance_surface, (50, WINDOW_HEIGHT - 20)
            )  # Adjust position as needed

            pygame.display.flip()  # Update the display with text
            time.sleep(5)  # Show the screen with distances for 5 seconds
            pygame.quit()
            return
        else:
            time.sleep(0.05)  # Wait half a second to visualize the movement


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
