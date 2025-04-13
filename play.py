import pygame
from minesweeper_grid import load_all_game_states

# Constants
CELL_SIZE = 20
GRID_SIZE = (40, 40)
FONT_SIZE = 16
FPS = 30

LIGHT_EDGE = (220, 220, 220)  # light for top/left edges
DARK_EDGE = (100, 100, 100)   # dark for bottom/right edges
NUMBER_BG = (144, 144, 144)   # darker gray for numbers

# Colors
BG_COLOR = (160, 160, 160)  # background of cells
BORDER_COLOR = (80, 80, 80)

TEXT_COLORS = {
    '1': (0, 0, 255),
    '2': (0, 128, 0),
    '3': (255, 0, 0),
    '4': (0, 0, 128),
    '5': (128, 0, 0),
    '6': (0, 128, 128),
    '7': (0, 0, 0),
    '8': (128, 128, 128),
}

# Load game states
game_states = load_all_game_states('frames', grid_size=GRID_SIZE, mine_density=0.30)
total_frames = len(game_states)

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE))
pygame.display.set_caption("Minesweeper Frame Player")
font = pygame.font.SysFont('Consolas', FONT_SIZE)
clock = pygame.time.Clock()

# Load mine image
mine_image = pygame.image.load('mine.png')
mine_image = pygame.transform.scale(mine_image, (CELL_SIZE - 4, CELL_SIZE - 4))

frame_idx = 0
play = True

def draw_grid(grid):
    screen.fill((0, 0, 0))
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if cell == '#':
                # Draw 3D button (raised)
                pygame.draw.rect(screen, BG_COLOR, rect)
                pygame.draw.line(screen, LIGHT_EDGE, (x, y), (x + CELL_SIZE - 1, y))  # top
                pygame.draw.line(screen, LIGHT_EDGE, (x, y), (x, y + CELL_SIZE - 1))  # left
                pygame.draw.line(screen, DARK_EDGE, (x, y + CELL_SIZE - 1), (x + CELL_SIZE - 1, y + CELL_SIZE - 1))  # bottom
                pygame.draw.line(screen, DARK_EDGE, (x + CELL_SIZE - 1, y), (x + CELL_SIZE - 1, y + CELL_SIZE - 1))  # right

            else:
                # Opened or number
                if cell.isdigit():
                    pygame.draw.rect(screen, NUMBER_BG, rect)
                else:
                    pygame.draw.rect(screen, BG_COLOR, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

                if cell == 'M':
                    screen.blit(mine_image, (x + 2, y + 2))
                elif cell.isdigit():
                    color = TEXT_COLORS.get(cell, (0, 0, 0))
                    text_surface = font.render(cell, True, color)
                    screen.blit(text_surface, (x + 5, y + 2))



running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play
            elif event.key == pygame.K_RIGHT:
                frame_idx = (frame_idx + 1) % total_frames
            elif event.key == pygame.K_LEFT:
                frame_idx = (frame_idx - 1) % total_frames

    if play:
        frame_idx = (frame_idx + 1) % total_frames

    draw_grid(game_states[frame_idx])
    pygame.display.flip()

pygame.quit()
