#Мне помогала ИИ а точнее Клод, но логику я проробатывал сам, и при чтении кода я все понимаю 

import pygame
import random

pygame.init()


MAZE = [
    "###################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#.......EEE.......#",
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
ENEMY_SPEED = 2       

WIDTH = len(MAZE[0]) * TILE
HEIGHT = len(MAZE) * TILE + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


def is_free(col, row):
    """True, если в клетке нет стены."""
    return MAZE[row][col] != "#"


def new_game():
    global px, py, dx, dy, next_dx, next_dy, dots, enemies, score, state
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
            if event.key == pygame.K_LEFT:
                next_dx, next_dy = -1, 0
            if event.key == pygame.K_RIGHT:
                next_dx, next_dy = 1, 0
            if event.key == pygame.K_UP:
                next_dx, next_dy = 0, -1
            if event.key == pygame.K_DOWN:
                next_dx, next_dy = 0, 1
            if event.key == pygame.K_r and state != "play":
                new_game()

    if state == "play":
    
     
        if (next_dx, next_dy) == (-dx, -dy):
            dx, dy = next_dx, next_dy

     
        if px % TILE == 0 and py % TILE == 0:
            col, row = px // TILE, py // TILE

            if (col, row) in dots:
                dots.remove((col, row))
                score += 10

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

      
        player_rect = pygame.Rect(px, py, TILE, TILE).inflate(-10, -10)
        for e in enemies:
            if player_rect.colliderect(pygame.Rect(e["x"], e["y"], TILE, TILE)):
                state = "lose"

        if not dots:
            state = "win"

   
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
    for e in enemies:
        pygame.draw.rect(screen, "#1d3557",
                         (e["x"] + 3, e["y"] + 6, TILE - 6, TILE - 9), border_radius=6)
        left, right = ("red", "#4cc9f0") if siren else ("#4cc9f0", "red")
        pygame.draw.rect(screen, left, (e["x"] + 7, e["y"] + 2, 8, 5), border_radius=2)
        pygame.draw.rect(screen, right, (e["x"] + 15, e["y"] + 2, 8, 5), border_radius=2)
        for eye in (11, 19):
            pygame.draw.circle(screen, "white", (e["x"] + eye, e["y"] + 15), 3)
            pygame.draw.circle(screen, "black",
                               (e["x"] + eye + e["dx"], e["y"] + 15 + e["dy"]), 2)

    screen.blit(font.render(f"Score: {score}", True, "white"),
                (10, len(MAZE) * TILE + 10))

    if state != "play":
        text = "You win!" if state == "win" else "Game Over"
        msg = font.render(f"{text}   (R - restart)", True, "yellow")
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()