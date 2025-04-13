import os
import cv2
import numpy as np
import time
import random

char = ["#","$","!","%","0","?","X"]

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
                row.append(" ")  # opened
            else:
                row.append("#")
                #row.append(random.choice(char))  # unopened
        grid.append(row)
    return grid

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_animation_from_folder(folder_path, grid_size, delay=0.1):
    frames = sorted(os.listdir(folder_path))
    frames = [f for f in frames if f.endswith(('.png', '.jpg', '.jpeg'))]

    for frame_file in frames:
        frame_path = os.path.join(folder_path, frame_file)
        grid = image_to_minesweeper_grid(frame_path, grid_size)
        clear_screen()
        for row in grid:
            print(' '.join(row))
        time.sleep(delay)

# Example usage (44 58)
play_animation_from_folder('frames', grid_size=(40, 40), delay=0.03)
