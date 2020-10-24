import pygame
import time
import random
pygame.init()

SQUARE_SIZE = 15 # size of grid square including border
CELL_SIZE = SQUARE_SIZE - 1 # sub 1 so cells aren't touching
CELLS_ACROSS = 100
CELLS_DOWN = 60
START_BUTTON_WIDTH = 100
START_BUTTON_HEIGHT = 30
RANDOM_BUTTON_WIDTH = 100
RANDOM_BUTTON_HEIGHT = 30
SCREEN_WIDTH = (CELLS_ACROSS * SQUARE_SIZE) + 1
SCREEN_HEIGHT = (CELLS_DOWN * SQUARE_SIZE) + 1 + START_BUTTON_HEIGHT + 10 # add 10 so button has 5 padding above and below
START_BUTTON_X = (SCREEN_WIDTH / 2) - START_BUTTON_WIDTH - 10
START_BUTTON_Y = SCREEN_HEIGHT - START_BUTTON_HEIGHT - 5
RANDOM_BUTTON_X = (SCREEN_WIDTH / 2) + 10
RANDOM_BUTTON_Y = SCREEN_HEIGHT - RANDOM_BUTTON_HEIGHT - 5

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((255,255,255))
pygame.display.set_caption('Game of Life')

# False if cell is dead, True if cell is alive
cells = [[False for _ in range(CELLS_ACROSS)] for _ in range(CELLS_DOWN)]
positions = []

# colors for alive and dead cells
colors = {
    True: (0,255,0),
    False: (0,0,0)
}

# tells whether the game of life rules should be checked each time step or
# if the user is just drawing cells
running = False

# set positions
for i in range(CELLS_DOWN):
    row = []
    for j in range(CELLS_ACROSS):
        row.append((j * SQUARE_SIZE + 1, i * SQUARE_SIZE + 1)) # add 1 so cells aren't touching

    positions.append(row)

# determine what got clicked and handle it appropriately
def handle_click(x_pos, y_pos):
    if y_pos > CELLS_DOWN * SQUARE_SIZE:
        # y pos is greater than height of grid, so only check if the start button was clicked
        check_button_clicked(x_pos, y_pos)
    else:
        check_cell_clicked(x_pos, y_pos)

# check if the click happended within the bounds of the start button
def check_button_clicked(x_pos, y_pos):
    global running

    if (x_pos >= START_BUTTON_X and x_pos <= START_BUTTON_X + START_BUTTON_WIDTH and 
            y_pos >= START_BUTTON_Y and y_pos <= START_BUTTON_Y + START_BUTTON_HEIGHT):
        running = not running
    elif (x_pos >= RANDOM_BUTTON_X and x_pos <= RANDOM_BUTTON_X + RANDOM_BUTTON_WIDTH and 
            y_pos >= RANDOM_BUTTON_Y and y_pos <= RANDOM_BUTTON_Y + RANDOM_BUTTON_HEIGHT):
        # randomize cell values
        for i in range(CELLS_DOWN):
            for j in range(CELLS_ACROSS):
                cells[i][j] = random.choice([True, False])

# check if the click happened within the bounds of a cell
def check_cell_clicked(x_pos, y_pos):
    # y pos is within grid, so check which cell got clicked
    for i in range(CELLS_DOWN):
        for j in range(CELLS_ACROSS):
            pos = positions[i][j]
            if (x_pos >= pos[0] and x_pos <= pos[0] + CELL_SIZE and 
                    y_pos >= pos[1] and y_pos <= pos[1] + CELL_SIZE):
                cells[i][j] = not cells[i][j]
                return

def game_of_life_rules():
    global cells

    temp_cells = [[False for _ in range(CELLS_ACROSS)] for _ in range(CELLS_DOWN)]
    for i in range(CELLS_DOWN):
        for j in range(CELLS_ACROSS):
            # print(f'{i}, {j} - {cells[i][j]}')
            if cells[i][j]:
                temp_cells[i][j] = get_new_alive_cell_value(i, j)
            else:
                temp_cells[i][j] = get_new_dead_cell_value(i, j)

    cells = temp_cells

def get_new_alive_cell_value(i, j):
    num_alive_neighbors = get_num_alive_neighbors(i, j)
    # print('----')
    # print(cells[i][j])
    # check rules for alive cells
    if num_alive_neighbors == 2 or num_alive_neighbors == 3:
        return True
    
    return False

def get_new_dead_cell_value(i, j):
    num_alive_neighbors = get_num_alive_neighbors(i, j)

    # check rule for dead cells
    if num_alive_neighbors == 3:
        return True

    return False

# Given the current cell, find all neighbors. Apply any screen wrapping needed
def get_neighbors(i, j):
    # positions of neighbors; index 0 = row, index 1 = column
    neighbors = {
        'down': [i+1, j],
        'left_down': [i+1, j-1],
        'left': [i, j-1],
        'left_up': [i-1, j-1],
        'up': [i-1, j],
        'right_up': [i-1, j+1],
        'right': [i, j+1],
        'right_down': [i+1, j+1]
    }

    # Check if neighbors are out of bounds. If they are, wrap to the other side of the screen
    if i <= 0:
        # wrap neighbors above to bottom of screen
        neighbors['left_up'][0] = CELLS_DOWN - 1
        neighbors['up'][0] = CELLS_DOWN - 1
        neighbors['right_up'][0] = CELLS_DOWN - 1
    elif i >= CELLS_DOWN - 1:
        # wrap neighbors below to top of screen
        neighbors['down'][0] = 0
        neighbors['left_down'][0] = 0
        neighbors['right_down'][0] = 0
    if j <= 0:
        # wrap left neighbors to right side of screen
        neighbors['left_down'][1] = CELLS_ACROSS -1
        neighbors['left'][1] = CELLS_ACROSS - 1
        neighbors['left_up'][1] = CELLS_ACROSS - 1
    elif j >= CELLS_ACROSS - 1:
        # wrap right neighbors to left side of screen
        neighbors['right_up'][1] = 0
        neighbors['right'][1] = 0
        neighbors['right_down'][1] = 0
        

    return neighbors

# find the number of living cells adjacent to the current cell
def get_num_alive_neighbors(i, j):
    neighbors = get_neighbors(i, j)
    num_alive = 0

    for key in neighbors.keys():
        neighbor_pos = neighbors[key]
        if cells[neighbor_pos[0]][neighbor_pos[1]]:
            num_alive += 1

    return num_alive

def draw_grid():
    for i in range(CELLS_DOWN):
        for j in range(CELLS_ACROSS):
            pos = positions[i][j]
            pygame.draw.rect(screen, colors[cells[i][j]], (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_buttons():
    # need to add text to button
    pygame.draw.rect(screen, (0,200,255), (START_BUTTON_X, START_BUTTON_Y, START_BUTTON_WIDTH, START_BUTTON_HEIGHT))
    pygame.draw.rect(screen, (0,225,175), (RANDOM_BUTTON_X, RANDOM_BUTTON_Y, RANDOM_BUTTON_WIDTH, RANDOM_BUTTON_HEIGHT))

def main_loop():
    done = False
    draw_buttons()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(event.pos[0], event.pos[1])
            
            if event.type == pygame.QUIT:
                done = True

        if running:
            game_of_life_rules()
            time.sleep(0.05)
        draw_grid()
        pygame.display.update()

main_loop()
pygame.quit()
quit()
