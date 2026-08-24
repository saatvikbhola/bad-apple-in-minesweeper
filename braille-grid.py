import os
import cv2
import numpy as np
import time

# The exact binary values for the 2x4 Braille dot layout
BRAILLE_WEIGHTS = np.array([
    [1, 8],
    [2, 16],
    [4, 32],
    [64, 128]
])

def image_to_braille_grid(image_path, term_grid_size, use_color=True, threshold=128, brightness_alpha=1.5, brightness_beta=20):
    term_h, term_w = term_grid_size
    
    # Since each braille char is a 2x4 grid, the actual image needs to be 
    # 2x wider and 4x taller than the terminal character count.
    img_w = term_w * 2
    img_h = term_h * 4
    
    # Read the image and immediately fix OpenCV's default BGR color space to RGB
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        return []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # --- BOOST BRIGHTNESS AND CONTRAST ---
    # alpha handles contrast (multiplier), beta adds flat brightness
    img_rgb = cv2.convertScaleAbs(img_rgb, alpha=brightness_alpha, beta=brightness_beta)
    
    # Resize the image to exactly match the mathematical limits of our Braille grid
    resized = cv2.resize(img_rgb, (img_w, img_h), interpolation=cv2.INTER_AREA)
    
    # Create a pure black and white (binary) mask to determine which dots are "On"
    gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, threshold, 1, cv2.THRESH_BINARY)
    
    # --- NUMPY MAGIC FOR MAXIMUM SPEED ---
    # Break the image into groups of 2x4 chunks
    b_chunks = binary.reshape(term_h, 4, term_w, 2).transpose(0, 2, 1, 3)
    
    # Multiply the chunks by the Braille binary values and sum them up
    braille_values = (b_chunks * BRAILLE_WEIGHTS).sum(axis=(2, 3))
    
    # Find the average RGB color of each 2x4 chunk for text coloring
    if use_color:
        c_chunks = resized.reshape(term_h, 4, term_w, 2, 3).transpose(0, 2, 1, 3, 4)
        colors = c_chunks.mean(axis=(2, 3)).astype(int)
    
    # --- RENDER STRINGS ---
    grid = []
    for i in range(term_h):
        row_chars = []
        for j in range(term_w):
            # 0x2800 is the blank Braille space. Add our calculated value to it.
            char = chr(0x2800 + int(braille_values[i, j]))
            
            if use_color:
                r, g, b = colors[i, j]
                # Apply ANSI true-color formatting
                row_chars.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
            else:
                row_chars.append(char)
                
        grid.append(''.join(row_chars))
        
    return grid

def play_animation_from_folder(folder_path, term_grid_size, delay=0.1, use_color=True, threshold=128, brightness_alpha=1.5, brightness_beta=20):
    frames = sorted(os.listdir(folder_path))
    # Filter for standard image formats
    frames = [f for f in frames if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Clear the screen completely once before the loop starts
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for frame_file in frames:
        frame_path = os.path.join(folder_path, frame_file)
        
        # Generate the text
        grid = image_to_braille_grid(frame_path, term_grid_size, use_color, threshold, brightness_alpha, brightness_beta)
        
        # Render the text using the cursor reset trick to prevent flickering
        print("\033[H", end="")
        print('\n'.join(grid))
        
        time.sleep(delay)

# Adjusted function call: Includes brightness_alpha (1.5 for 50% boost) and brightness_beta (20 for flat boost)
play_animation_from_folder(
    'odyssey-frames', 
    term_grid_size=(50, 178), 
    delay=0.03, 
    use_color=True, 
    threshold=5,
    brightness_alpha=1.5, 
    brightness_beta=20
)
