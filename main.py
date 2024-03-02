from utils import *

selected_color = BLACK


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Program")


def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                                          PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 25, 25, BLACK, background_color=BLACK),
    Button(10, button_y + 25, 25, 25, RED, background_color=RED),
    Button(35, button_y, 25, 25, GREEN, background_color=GREEN),
    Button(35, button_y + 25, 25, 25, BLUE, background_color=BLUE),
    Button(80, button_y - 5, 75, 30, WHITE, "Eraser", BLACK),
    Button(80, button_y + 30, 75, 30, WHITE, "Clear", BLACK),
    Button(160, button_y - 5, 75, 30, WHITE, "Move", BLACK),
    Button(160, button_y + 30, 75, 30, WHITE, "Rotate", BLACK),
    Button(240, button_y - 5, 75, 30, WHITE, "Resize", BLACK),
    Button(240, button_y + 30, 75, 30, WHITE, "Reflex", BLACK),
    Button(320, button_y - 5, 75, 30, WHITE, "DDA", BLACK),
    Button(320, button_y + 30, 75, 30, WHITE, "Bres", BLACK),
    Button(400, button_y - 5, 75, 30, WHITE, "C-S", BLACK),
    Button(400, button_y + 30, 75, 30, WHITE, "L-B", BLACK),
    Button(480, button_y - 5, 75, 30, WHITE, "Circle", BLACK)

]

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        # If user clicks the close window button
        if event.type == pygame.QUIT:
            run = False


        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)
                grid[row][col] = drawing_color
            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue

                    drawing_color = button.color

                    if not button.background_color == WHITE:
                        selected_color = drawing_color

                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK

    draw(WIN, grid, buttons)

pygame.quit()
