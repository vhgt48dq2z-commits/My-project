import pygame

pygame.init()

# ---------- Настройки (меняй под себя) ----------
MAP_FILE = "pacman.png"
GHOST_FILE = "images.png"      # поменяй на имя своей картинки призрака
GHOST_SIZE = 40               # размер призрака в пикселях
SPEED = 4
FPS = 60
WALLS_ON = True  
MAP_SCALE = 1.5             # False = призрак проходит сквозь стены


# ---------- Окно и картинки ----------
map_img = pygame.image.load(MAP_FILE)
w, h = map_img.get_size()
WIDTH, HEIGHT = int(w * MAP_SCALE), int(h * MAP_SCALE)   # новый размер окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman: призрак")
clock = pygame.time.Clock()

map_img = map_img.convert()
map_img = pygame.transform.scale(map_img, (WIDTH, HEIGHT))   # растягиваем карту
ghost = pygame.image.load(GHOST_FILE).convert_alpha()
ghost = pygame.transform.scale(ghost, (GHOST_SIZE, GHOST_SIZE))


# ---------- Стены ----------
def is_wall_pixel(px, py):
    """Стена = синий пиксель. Если у тебя другие цвета, поменяй условие."""
    if px < 0 or py < 0 or px >= WIDTH or py >= HEIGHT:
        return True                          # за границей карты тоже стена
    r, g, b, *_ = map_img.get_at((px, py))
    return b > 150 and r < 100 and g < 100


def is_blocked(x, y):
    """Проверяем углы и середины сторон хитбокса призрака."""
    m = 4                                    # небольшой отступ, чтобы не цеплялся за края
    left, top = x + m, y + m
    right, bottom = x + GHOST_SIZE - m, y + GHOST_SIZE - m
    cx, cy = (left + right) // 2, (top + bottom) // 2
    points = [(left, top), (right, top), (left, bottom), (right, bottom),
              (cx, top), (cx, bottom), (left, cy), (right, cy)]
    return any(is_wall_pixel(px, py) for px, py in points)


def find_free_spot():
    """Ищем свободное место ближе всего к центру карты."""
    best, best_dist = (0, 0), None
    for sy in range(0, HEIGHT - GHOST_SIZE, 4):
        for sx in range(0, WIDTH - GHOST_SIZE, 4):
            if not is_blocked(sx, sy):
                d = (sx - WIDTH // 2) ** 2 + (sy - HEIGHT // 2) ** 2
                if best_dist is None or d < best_dist:
                    best, best_dist = (sx, sy), d
    return best


# ---------- Состояние призрака ----------
x, y = find_free_spot() if WALLS_ON else (WIDTH // 2, HEIGHT // 2)
facing_left = False

# ---------- Игровой цикл ----------
running = True
while running:
    # 1. События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Управление
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += SPEED

    if dx < 0:
        facing_left = True
    elif dx > 0:
        facing_left = False

    # 3. Движение: по осям отдельно, чтобы можно было скользить вдоль стены
    new_x = x + dx
    if not WALLS_ON or not is_blocked(new_x, y):
        x = new_x
    new_y = y + dy
    if not WALLS_ON or not is_blocked(x, new_y):
        y = new_y

    # Границы окна
    x = max(0, min(x, WIDTH - GHOST_SIZE))
    y = max(0, min(y, HEIGHT - GHOST_SIZE))

    # 4. Отрисовка: сначала карта, потом призрак
    screen.blit(map_img, (0, 0))
    image = pygame.transform.flip(ghost, True, False) if facing_left else ghost
    screen.blit(image, (x, y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
