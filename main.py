import pygame
import numpy as np

# Parameters for the simulation
size = 200  # Size of the grid
n_species = 3  # Number of different species
initial_creatures = 100  # Initial number of creatures
food_spawn_interval = 300  # Time interval for food spawning (in iterations)
food_spawn_amount = 20  # Number of food pixels to spawn at each interval
creature_speed = 1  # Speed at which creatures move
reproduction_threshold = 1  # Number of food pixels needed for reproduction
max_lifespan = 1000  # Maximum lifespan of a cell
max_hunger = 500  # Maximum hunger value of a cell
hunger_decrease = 1  # Amount by which hunger decreases in each iteration
lifespan_decrease = 1  # Amount by which lifespan decreases in each iteration
hunger_replenish = 300  # Amount by which hunger is replenished when a cell eats food
framerate = 30

# Calculate the cell size and window size based on desired dimensions
cell_size = 4
grid_size = size * cell_size
table_size = 320
window_width = grid_size + table_size
window_height = grid_size

# Colors for each species
colors = [
    (255, 255, 255),  # Empty cell (white)
    (255, 0, 0),  # Species 1 (red)
    (0, 255, 0),  # Species 2 (green)
    (0, 0, 255),  # Species 3 (blue)
]
# Initialize the grid with random creatures
indices = np.random.choice(np.arange(size ** 2), size=initial_creatures, replace=False)
x, y = np.unravel_index(indices, (size, size))

class Food:
    def __init__(self):
        self.pos = [0,0]
class Cell:
    def __init__(self):
        self.species = np.random.choice(range(1, n_species + 1))  # Assign a random species to each cell
        self.color = colors[self.species]  # Get the color corresponding to the species
        self.pos = [0,0]
        self.currentLifespan = max_lifespan
        self.currentHunger = max_hunger

    def move(self):
        # Generate random movement direction
        dx = np.random.randint(-creature_speed, creature_speed + 1)
        dy = np.random.randint(-creature_speed, creature_speed + 1)

        # Update cell position
        self.pos[0] += dx
        self.pos[1] += dy

        # Keep the cell within the grid bounds
        self.pos[0] = np.clip(self.pos[0], 0, size - 1)
        self.pos[1] = np.clip(self.pos[1], 0, size - 1)

    def degrade(self):
        self.currentLifespan -= lifespan_decrease
        self.currentHunger -= hunger_decrease

    def naturalDeath(self):
        if self.currentLifespan <= 0 or self.currentHunger <=0:
            new_food = Food()  # Create an instance of the Food class
            new_food.pos = [self.pos[0], self.pos[1]]  # Set the position of the new food
            food.append(new_food)  # Append the new food to the food list
            cells.remove(self)

    def death(self):
        if self.currentLifespan <= 0 or self.currentHunger <= 0:
            cells.remove(self)

    def multiply(self):
        if True:
            new_cell = Cell()  # Create an instance of the Food class
            new_cell.pos = [self.pos[0], self.pos[1]]  # Set the position of the new food
            new_cell.species = self.species
            new_cell.color = colors[self.species]
            cells.append(new_cell)

cells = [Cell() for _ in range(initial_creatures)]
food = [Food() for _ in range(food_spawn_amount)]

for i in range(initial_creatures):
    cells[i].pos[0] = x[i]
    cells[i].pos[1] = y[i]
    cells[i].species = np.random.choice(range(1, n_species + 1))  # Assign a random species to each cell
    cells[i].color = colors[cells[i].species]  # Get the color corresponding to the species

for i in range(food_spawn_amount):
    food[i].pos[0] = x[i]
    food[i].pos[1] = y[i]

# Initialize Pygame
pygame.init()
pygame.display.set_caption('CellLife')
#icon = pygame.image.load('Background.png')
#pygame.display.set_icon(icon)
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Initialize food variables
food_timer = 0
cycle = 0
species_count = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # Create a surface for the grid
    surface = pygame.Surface((window_width - table_size, window_height))

    # Draw food pixels
    for i, f in enumerate(food):
        pygame.draw.rect(surface, colors[0], (f.pos[1] * cell_size, f.pos[0] * cell_size, cell_size, cell_size))

    # species_count = np.bincount(species.flatten())[1:]
    for i, cell in enumerate(cells):
        cell_rect = pygame.Rect(cell.pos[1] * cell_size, cell.pos[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, cell.color, cell_rect)

    # Draw the surface onto the screen
    screen.blit(surface, (0, 0))

    # Display the cell count and species count table
    table = pygame.Surface((table_size, window_height))
    table.fill((255, 255, 255))

    cycle += 1
    timeValue = int(cycle / framerate)

    text = font.render(f"Time[s]: {timeValue}", True, (0, 0, 0))
    table.blit(text, (10, 10))

    text = font.render(f"Cycle: {cycle}", True, (0, 0, 0))
    table.blit(text, (10, 40))

    text = font.render(f"Cell count: {len(cells)}", True, (0, 0, 0))
    table.blit(text, (10, 70))

    species = [cell.species for cell in cells]
    species_count = np.bincount(species)[1:]

    for i in range(n_species):
        text = font.render(f"Species {i + 1} Count: {species_count[i]}", True, (colors[i+1]))
        table.blit(text, (10, 100 + i * 30))

    screen.blit(table, (window_width - table_size, 0))
    pygame.display.flip()

    cellsNumber = len(cells)

    for cell in cells[:]:
        cell.move()
        cell.degrade()
        cell.naturalDeath()

        for food_item in food[:]:
            if cell.pos == food_item.pos and cell.currentHunger > 0 and cell.currentLifespan > 0:
                food.remove(food_item)
                cell.currentHunger += hunger_replenish
                cell.multiply()
                break

        # Check for contact with other cells
        for otherCell in cells[:]:
            if cell is not otherCell and cell.pos == otherCell.pos and cell.species != otherCell.species and cell.currentHunger > 0 and cell.currentLifespan > 0:
                otherCell.death()
                cells.remove(otherCell)
                cell.currentHunger += hunger_replenish
                cell.multiply()
                break

    # Spawn food periodically
    if food_timer % food_spawn_interval == 0:
        indices = np.random.choice(np.arange(size ** 2), size=food_spawn_amount, replace=False)
        x, y = np.unravel_index(indices, (size, size))
        for i in range(len(x)):
            new_food = Food()  # Create an instance of the Food class
            new_food.pos = [x[i], y[i]]  # Set the position of the new food
            food.append(new_food)  # Append the new food to the food list

    # Increment the food timer
    food_timer += 1

    # Control the speed of the simulation
    clock.tick(framerate)

pygame.quit()
