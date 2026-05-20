import random
import pygame

pygame.init()

# ——— window setup ———
WIDTH, HEIGHT = 500, 500
UI_HEIGHT = 120
GRID_HEIGHT = HEIGHT - UI_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morph Memory")

BG = (255, 255, 255)
GRID = (200, 200, 200)
FILLED = (50, 150, 255)

font = pygame.font.SysFont(None, 28)

# ——— game settings ———
grid_size = 5
max_size = 8
lives = 3
score = 0

instruction_text = ""
status_text = "Press SPACE to start"


# ——— GRID DRAWING ———
def print_grid(size, pattern):
    screen.fill(BG)

    cell_size = GRID_HEIGHT // size
    grid_pixel_size = cell_size * size

    offset_x = (WIDTH - grid_pixel_size) // 2
    offset_y = (GRID_HEIGHT - grid_pixel_size) // 2

    for r in range(size):
        for c in range(size):
            rect = pygame.Rect(
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size,
                cell_size
            )

            if (r, c) in pattern:
                pygame.draw.rect(screen, FILLED, rect)
            else:
                pygame.draw.rect(screen, GRID, rect, 1)

    draw_ui()
    pygame.display.update()


# ——— UI ———
def draw_ui():
    pygame.draw.rect(screen, (240, 240, 240), (0, GRID_HEIGHT, WIDTH, UI_HEIGHT))

    y = GRID_HEIGHT + 10

    if instruction_text:
        text = font.render("Instruction: " + instruction_text, True, (0, 0, 0))
        screen.blit(text, (10, y))

    text2 = font.render(
        f"Score: {score}  Lives: {lives}  Grid: {grid_size}",
        True,
        (0, 0, 0)
    )
    screen.blit(text2, (10, y + 30))

    text3 = font.render(status_text, True, (0, 0, 0))
    screen.blit(text3, (10, y + 60))


# ——— pattern generation ———
def make_pattern(size):
    pattern = []
    first = (random.randint(0, size - 1), random.randint(0, size - 1))
    pattern.append(first)

    target = random.randint(2, 5)

    while len(pattern) < target:
        base = random.choice(pattern)
        r, c = base

        neighbors = [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]

        added = False
        for nr, nc in neighbors:
            if 0 <= nr < size and 0 <= nc < size:
                if (nr, nc) not in pattern:
                    pattern.append((nr, nc))
                    added = True
                    break

        if not added:
            rand_cell = (random.randint(0, size - 1),
                         random.randint(0, size - 1))
            if rand_cell not in pattern:
                pattern.append(rand_cell)

    return pattern


# ——— transformations ———
def rotate(pattern, size):
    return [(c, size - 1 - r) for r, c in pattern]


def flip(pattern, size):
    return [(r, size - 1 - c) for r, c in pattern]


def move(pattern, dr, dc):
    return [(r + dr, c + dc) for r, c in pattern]


def valid(pattern, size):
    return all(0 <= r < size and 0 <= c < size for r, c in pattern)


def transform(pattern, size, difficulty):
    while True:
        temp = pattern[:]
        text_parts = []

        steps = 1 if difficulty < 3 else random.choice([1, 2])

        direction_map = {
            (-1, -1): "up-left",
            (-1, 0): "up",
            (-1, 1): "up-right",
            (0, -1): "left",
            (0, 1): "right",
            (1, -1): "down-left",
            (1, 0): "down",
            (1, 1): "down-right",
        }

        for _ in range(steps):
            choice = random.choice(["rotate", "flip", "move"])

            if choice == "rotate":
                temp = rotate(temp, size)
                text_parts.append("rotate 90°")

            elif choice == "flip":
                temp = flip(temp, size)
                text_parts.append("flip")

            else:
                dr = random.randint(-1, 1)
                dc = random.randint(-1, 1)

                while dr == 0 and dc == 0:
                    dr = random.randint(-1, 1)
                    dc = random.randint(-1, 1)

                temp = move(temp, dr, dc)
                text_parts.append(f"shift {direction_map[(dr, dc)]}")

        if valid(temp, size):
            return temp, " + ".join(text_parts)


# ——— INPUT (toggle fixed) ———
def get_input(size):
    user = []

    cell_size = GRID_HEIGHT // size
    grid_pixel_size = cell_size * size

    offset_x = (WIDTH - grid_pixel_size) // 2
    offset_y = (GRID_HEIGHT - grid_pixel_size) // 2

    global status_text
    status_text = "Click cells, press ENTER when done"

    done = False

    while not done:
        print_grid(size, user)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if y < GRID_HEIGHT:
                    c = (x - offset_x) // cell_size
                    r = (y - offset_y) // cell_size

                    if 0 <= r < size and 0 <= c < size:
                        cell = (r, c)

                        # toggle logic
                        if cell in user:
                            user.remove(cell)
                        else:
                            user.append(cell)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True

    return user


# ——— MAIN GAME ———
def play_game():
    global grid_size, score, lives, instruction_text, status_text

    running = True
    started = False
    difficulty = 0

    while running:

        screen.fill(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not started:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True

        if not started:
            status_text = "Press SPACE to start"
            draw_ui()
            pygame.display.update()
            continue

        status_text = "Memorize the pattern"

        pattern = make_pattern(grid_size)
        print_grid(grid_size, pattern)

        pygame.time.delay(3000)

        screen.fill(BG)
        pygame.display.update()

        new_pattern, instruction_text = transform(pattern, grid_size, difficulty)

        user_answer = get_input(grid_size)

        if set(user_answer) == set(new_pattern):
            status_text = "Correct!"
            score += 1
            difficulty += 1

            if score % 2 == 0 and grid_size < max_size:
                grid_size += 1

        else:
            status_text = "Wrong! Showing answer..."
            print_grid(grid_size, new_pattern)
            pygame.time.delay(2000)
            lives -= 1

        pygame.time.delay(1000)

        if lives <= 0:
            status_text = f"Game Over! Final Score: {score}"
            draw_ui()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

    pygame.quit()


play_game()