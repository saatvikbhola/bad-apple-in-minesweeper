import cv2
import numpy as np
import random
import os
from tqdm import tqdm  # Progress bar

def image_to_minesweeper_grid(image_path, grid_size):
    # Load grayscale image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # Step 1: Canny edge detection
    edges = cv2.Canny(img, threshold1=50, threshold2=150)

    # Step 2: Dilate edges to make them thicker (edge thickness = 2)
    kernel = np.ones((5, 5), np.uint8)  # 2x2 kernel for thickness
    thick_edges = cv2.dilate(edges, kernel, iterations=1)

    # Calculate cell size
    cell_h = height // grid_size[0]
    cell_w = width // grid_size[1]

    grid = []
    for i in range(grid_size[0]):
        row = []
        for j in range(grid_size[1]):
            cell_img = img[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            cell_edge = thick_edges[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]

            avg_color = np.mean(cell_img)
            edge_present = np.mean(cell_edge) > 20  # if there are enough edge pixels in cell

            if edge_present:
                row.append('X')  # thickened edge = unopened
            elif avg_color < 50:
                row.append(' ')  # black = opened
            else:
                row.append('#')  # light area = unopened
        grid.append(row)
    return grid

def generate_minesweeper_state_from_mask(mask_grid, mine_density=0.3):
    rows, cols = len(mask_grid), len(mask_grid[0])
    state_grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    # Only allow mines on '#' cells (not 'X' or already opened ' ')
    unopened_cells = [
        (i, j)
        for i in range(1, rows - 1)
        for j in range(1, cols - 1)
        if mask_grid[i][j] == '#'
    ]

    num_mines = int(len(unopened_cells) * mine_density)
    mine_positions = set(random.sample(unopened_cells, num_mines))

    # Step 1: Place mines
    for i, j in mine_positions:
        state_grid[i][j] = 'M'

    # Step 2: Process numbers
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

    # Step 3: Preserve edge cells from mask as 'X'
    for i in range(rows):
        for j in range(cols):
            if mask_grid[i][j] == 'X':
                state_grid[i][j] = 'X'

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