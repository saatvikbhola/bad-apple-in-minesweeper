## 1. Overview

This project uses a set of Python scripts to convert a standard video file into two types of animations:

1.  **Terminal Grid Animation**: A text-based animation that plays directly in your console.
2.  **Minesweeper Animation**: A graphical animation that visualizes the video frames as a series of Minesweeper boards, rendered in a Pygame window.

## 2. Workflow

### Workflow 1: Terminal Grid Animation

1.  **`frames.py`**: Extracts frames from a video file.
2.  **`grid.py`**: Converts each frame into a text grid and prints it to the console.

### Workflow 2: Minesweeper Animation (Graphical)

1.  **`frames.py`**: Extracts frames from a video file.
2.  **`minesweeper_utils.py`**: Converts each frame into a Minesweeper board state, complete with mines and numbers.
3.  **`play.py`**: Renders the sequence of Minesweeper boards as a graphical animation using Pygame.

## 3. Requirements

Before running the scripts, you need to install the necessary Python libraries.

```
pip install opencv-python tqdm numpy pygame
```

* **`opencv-python`**, **`tqdm`**, **`numpy`**: Required for the core video processing.
* **`pygame`**: Required only for the graphical Minesweeper animation.

## 4. Usage

### Running the Terminal Animation

1.  Run `frames.py` to extract images from your video into the `frames/` folder.
2.  Run `grid.py` to play the animation in your terminal.

https://github.com/user-attachments/assets/087adaf9-170e-4475-9653-4b820baf719a

### Running the Minesweeper Animation

1.  Ensure you have a `mine.png` image file in the same directory.
2.  Run `frames.py` to extract images from your video into the `frames/` folder.
3.  Run `play.py` to start the graphical animation in a new window. (this takes time to run completly.)
    * Press **SPACE** to play/pause the animation.
    * Use the **LEFT/RIGHT ARROW KEYS** to step through frames manually.

## 5. File Documentation

### `frames.py`

* **Purpose**: Extracts frames from a video file and saves them as images.

### `grid.py` (For Terminal Animation)

* **Purpose**: Creates a text-based animation in the terminal from image frames.

### `minesweeper_utils.py` (For Minesweeper Animation)

* **Purpose**: Contains the core logic for converting an image frame into a complete Minesweeper board state.
* **Key Function**: `load_all_game_states(...)` processes a folder of frames and generates a list of Minesweeper grids, intelligently placing mines and calculating numbers based on the image's content and edges.

#### Key Functions in `minesweeper_utils.py`

The conversion from an image to a Minesweeper board happens in a two-step process, orchestrated by a primary function:

1.  **`image_to_minesweeper_grid(image_path, grid_size)`**:
    * **Purpose**: This function creates an initial "mask" from the image. It analyzes the image for edges and brightness to decide the basic structure of the board for that frame.
    * **Process**: It uses Canny edge detection to find outlines. Cells that are part of a detected edge are marked as `X` (a border), dark areas of the image are marked as ` ` (already revealed), and the remaining areas are marked as `#` (unrevealed).
    * **Output**: A 2D list representing the structural mask of the board.

2.  **`generate_minesweeper_state_from_mask(mask_grid, mine_density)`**:
    * **Purpose**: This function takes the structural mask and turns it into a playable Minesweeper state.
    * **Process**: It randomly places mines (`M`) only on the cells marked as `#` in the mask. Then, for all remaining `#` cells, it calculates the number of adjacent mines and fills in the corresponding number (`1`, `2`, etc.). It leaves the `X` and ` ` cells as they are.
    * **Output**: A final 2D list representing a complete Minesweeper board for one frame.

3.  **`load_all_game_states(frames_folder, grid_size, mine_density)`**:
    * **Purpose**: This is the main utility function called by `play.py`. It manages the entire conversion process for all frames.
    * **Process**: It iterates through every image in the specified `frames_folder`, calls the two functions above for each image, and collects the final board states into a single list.
    * **Output**: A list containing all the generated Minesweeper board states, ready for animation.

### `play.py` (For Minesweeper Animation)

* **Purpose**: The main script for the graphical animation. It loads the Minesweeper states and uses Pygame to render them in a window with interactive controls.
