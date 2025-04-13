import cv2
import numpy as np
import random
import os
from tqdm import tqdm  # Progress bar

def image_to_minesweeper_grid(image_path, grid_size):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    cell_h = height // grid_size[0]
    cell_w = width // grid_size[1]

    grid = []
    for i in range(grid_size[0]):
        row = []
        for j in range(grid_size[1]):
            cell = img[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            avg_color = np.mean(cell)
            if avg_color < 50:
                row.append(' ')
            else:
                row.append('#')
        grid.append(row)
    return grid

def generate_minesweeper_state_from_mask(mask_grid, mine_density=0.3):
    rows, cols = len(mask_grid), len(mask_grid[0])
    state_grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    unopened_cells = [
        (i, j)
        for i in range(1, rows - 1)
        for j in range(1, cols - 1)
        if mask_grid[i][j] == '#'
    ]

    num_mines = int(len(unopened_cells) * mine_density)
    mine_positions = set(random.sample(unopened_cells, num_mines))

    for i, j in mine_positions:
        state_grid[i][j] = 'M'

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if mask_grid[i][j] == '#' and state_grid[i][j] != 'M':
                count = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if (ni, nj) in mine_positions:
                            count += 1
                if count > 0:
                    state_grid[i][j] = str(count)
                else:
                    state_grid[i][j] = '#'

    return state_grid

def load_all_game_states(frames_folder='frames', grid_size=(40, 40), mine_density=0.3):
    frame_files = sorted(
        [f for f in os.listdir(frames_folder) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: int(''.join(filter(str.isdigit, x)))
    )

    game_states = []

    for frame_file in tqdm(frame_files, desc="Generating game states"):
        frame_path = os.path.join(frames_folder, frame_file)
        mask_grid = image_to_minesweeper_grid(frame_path, grid_size)
        state = generate_minesweeper_state_from_mask(mask_grid, mine_density)
        game_states.append(state)

    return game_states