# Мне помогала ИИ а точнее Клод, но логику я проробатывал сам, и при чтении кода я все понимаю

import math
import os
import random

import pygame

pygame.init()


MAZE = [
    "###################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#........E........#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.###.#.###.####",
    "#.................#",
    "####.#.#####.#.####",
    "#........P........#",
    "#.##.###.#.###.##.#",
    "#..#.....#.....#..#",
    "##.#.#.#####.#.#.##",
    "#....#...#...#....#",
    "###################",
]

TILE = 30
PLAYER_SPEED = 3
ENEMY_SPEED = 1

WIDTH = len(MAZE[0]) * TILE
HEIGHT = len(MAZE) * TILE + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_sound(filename, volume=1.0):

    path = os.path.join(BASE_DIR, filename)
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except (FileNotFoundError, pygame.error) as err:
        print(f"[звук] Не удалось загрузить {filename}: {err}")
        return None


def play(sound):

    if sound:
        sound.play()


CHASE_SOUND_FILES = [
    "salo.wav", "lose.wav"
]


chase_sounds = [s for s in (load_sound(f, 0.9) for f in CHASE_SOUND_FILES) if s]

print(f"[звук] Загружено звуков погони: {len(chase_sounds)} из {len(CHASE_SOUND_FILES)}")

CHASE_DISTANCE = 9 * TILE
VOICE_PAUSE = 800


pygame.mixer.set_reserved(1)
voice_channel = pygame.mixer.Channel(0)


eat_sound = load_sound("eat.wav", volume=0.3)


win_sound = load_sound("i-just-slap.wav", volume=0.9)
lose_sound = load_sound("here-our-powers-are-all.wav", volume=0.9)

def load_image(filename):
    path = os.path.join(BASE_DIR, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (TILE, TILE))
    except (FileNotFoundError, pygame.error) as err:
        print(f"[картинка] Не удалось загрузить {filename}: {err}")
        return None


IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
POLICE_IMAGE_FILES = sorted(
    f for f in os.listdir(BASE_DIR)
    if f.lower().startswith("police") and f.lower().endswith(IMAGE_EXTS)
)
police_imgs = [img for img in (load_image(f) for f in POLICE_IMAGE_FILES) if img]
print(f"[картинка] Найдено фоток полицейских: {len(police_imgs)} {POLICE_IMAGE_FILES}")


def is_free(col, row):
    return MAZE[row][col] != "#"


def new_game():
    global px, py, dx, dy, next_dx, next_dy, dots, enemies, score, state
    global voice_index, next_voice_time, was_chasing


    pygame.mixer.stop()
    voice_index = 0
    next_voice_time = 0
    was_chasing = False

    dots = set()
    enemies = []
    colors = ["#e63946", "#f4a261", "#9b5de5"]

    for row, line in enumerate(MAZE):
        for col, ch in enumerate(line):
            if ch == ".":
                dots.add((col, row))
            elif ch == "P":
                px, py = col * TILE, row * TILE
            elif ch == "E":
                enemies.append({"x": col * TILE, "y": row * TILE,
                                "dx": 0, "dy": 0,
                                "color": colors[len(enemies) % 3]})

    dx, dy = 0, 0
    next_dx, next_dy = 0, 0
    score = 0
    state = "play"


new_game()

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:

            key, scan = event.key, event.scancode

            if key in (pygame.K_LEFT, pygame.K_a) or scan == pygame.KSCAN_A:
                next_dx, next_dy = -1, 0
            if key in (pygame.K_RIGHT, pygame.K_d) or scan == pygame.KSCAN_D:
                next_dx, next_dy = 1, 0
            if key in (pygame.K_UP, pygame.K_w) or scan == pygame.KSCAN_W:
                next_dx, next_dy = 0, -1
            if key in (pygame.K_DOWN, pygame.K_s) or scan == pygame.KSCAN_S:
                next_dx, next_dy = 0, 1
            if (key == pygame.K_r or scan == pygame.KSCAN_R) and state != "play":
                new_game()

    if state == "play":

        if (next_dx, next_dy) == (-dx, -dy):
            dx, dy = next_dx, next_dy

        if px % TILE == 0 and py % TILE == 0:
            col, row = px // TILE, py // TILE

            if (col, row) in dots:
                dots.remove((col, row))
                score += 10
                play(eat_sound)

            if is_free(col + next_dx, row + next_dy):
                dx, dy = next_dx, next_dy
            if not is_free(col + dx, row + dy):
                dx, dy = 0, 0

        px += dx * PLAYER_SPEED
        py += dy * PLAYER_SPEED

        for e in enemies:
            if e["x"] % TILE == 0 and e["y"] % TILE == 0:
                col, row = e["x"] // TILE, e["y"] // TILE

                options = []
                for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if is_free(col + d[0], row + d[1]):
                        options.append(d)
                if len(options) > 1 and (-e["dx"], -e["dy"]) in options:
                    options.remove((-e["dx"], -e["dy"]))

                if random.random() < 0.5:
                    d = min(options, key=lambda d:
                            abs((col + d[0]) * TILE - px) + abs((row + d[1]) * TILE - py))
                else:
                    d = random.choice(options)
                e["dx"], e["dy"] = d

            e["x"] += e["dx"] * ENEMY_SPEED
            e["y"] += e["dy"] * ENEMY_SPEED


        chasing = any(math.hypot(e["x"] - px, e["y"] - py) < CHASE_DISTANCE
                      for e in enemies)


        was_chasing = chasing

        now = pygame.time.get_ticks()
        if (chasing and chase_sounds
                and not voice_channel.get_busy()
                and now >= next_voice_time):
            sound = chase_sounds[voice_index]
            voice_channel.play(sound)

            next_voice_time = now + int(sound.get_length() * 1000) + VOICE_PAUSE

            voice_index = (voice_index + 1) % len(chase_sounds)


        player_rect = pygame.Rect(px, py, TILE, TILE).inflate(-10, -10)
        for e in enemies:
            if player_rect.colliderect(pygame.Rect(e["x"], e["y"], TILE, TILE)):
                state = "lose"
                voice_channel.stop()
                play(lose_sound)
                break


        if state == "play" and not dots:
            state = "win"
            voice_channel.stop()
            play(win_sound)

    screen.fill("#0b0f1a")

    for row, line in enumerate(MAZE):
        for col, ch in enumerate(line):
            if ch == "#":
                pygame.draw.rect(screen, "#2b3a67",
                                 (col * TILE + 1, row * TILE + 1, TILE - 2, TILE - 2),
                                 border_radius=6)

    for col, row in dots:
        cx = col * TILE + TILE // 2
        cy = row * TILE + TILE // 2
        pygame.draw.rect(screen, "#f1e3c8", (cx - 2, cy, 4, 6))
        pygame.draw.ellipse(screen, "#e63946", (cx - 7, cy - 6, 14, 9))
        pygame.draw.circle(screen, "white", (cx - 3, cy - 3), 1)
        pygame.draw.circle(screen, "white", (cx + 3, cy - 2), 1)

    pygame.draw.circle(screen, "#3ddc84", (px + TILE // 2, py + TILE // 2), TILE // 2 - 3)

    siren = (pygame.time.get_ticks() // 150) % 2 == 0
    for i, e in enumerate(enemies):
        if police_imgs:

            img = police_imgs[i % len(police_imgs)]
            screen.blit(img, (e["x"], e["y"]))
        else:

            pygame.draw.rect(screen, "#1d3557",
                             (e["x"] + 3, e["y"] + 6, TILE - 6, TILE - 9), border_radius=6)
            for eye in (11, 19):
                pygame.draw.circle(screen, "white", (e["x"] + eye, e["y"] + 15), 3)
                pygame.draw.circle(screen, "black",
                                   (e["x"] + eye + e["dx"], e["y"] + 15 + e["dy"]), 2)


        left, right = ("red", "#4cc9f0") if siren else ("#4cc9f0", "red")
        pygame.draw.rect(screen, left, (e["x"] + 7, e["y"] + 2, 8, 5), border_radius=2)
        pygame.draw.rect(screen, right, (e["x"] + 15, e["y"] + 2, 8, 5), border_radius=2)

    screen.blit(font.render(f"Score: {score}", True, "white"),
                (10, len(MAZE) * TILE + 10))

    if state != "play":
        text = "You win!" if state == "win" else "Game Over"
        msg = font.render(f"{text}   (R - restart)", True, "yellow")
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()