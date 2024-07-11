import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga-inspired Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)

# Player
player_width = 20
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5
player_lives = 3
player_shoot_angle = 0  # Shooting direction angle

# Enemy
enemy_width = 20
enemy_height = 20
enemies = []

# Special circular alien ship
special_ship = {'x':0, 'y':0, 'speed':10, 'radius':30}
special_ship_spawn_timer = 0
SPECIAL_SHIP_SPAWN_INTERVAL = 30 * 60  # 30 seconds (60 frames per second)

# Bullets
bullet_width = 2
bullet_height = 2
player_bullets = []
enemy_bullets = []
bullet_speed = 7

# Game state
game_over = False
level_complete = False
current_level = 1
score = 0

# Font
font = pygame.font.Font(None, 36)

# High Scores
high_scores = []
SCORE_FILE = "high_scores.txt"

# Load images
player_img = pygame.image.load("player_ship.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))
enemy_img = pygame.image.load("enemy_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
special_ship_img = pygame.image.load("special_ship.png")
special_ship_img = pygame.transform.scale(special_ship_img, (60, 60))

# Sound effects
player_shoot_sound = pygame.mixer.Sound("sounds/player_shoot.wav")
enemy_shoot_sound = pygame.mixer.Sound("sounds/enemy_shoot.wav")
enemy_hit_sound = pygame.mixer.Sound("sounds/enemy_hit.wav")
player_hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
extra_life_sound = pygame.mixer.Sound("sounds/extra_life.wav")

# Background music
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def load_high_scores():
    global high_scores
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            high_scores = [int(score.strip()) for score in file.readlines()]
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10]  # Keep only top 10 scores

def save_high_scores():
    with open(SCORE_FILE, "w") as file:
        for score in high_scores:
            file.write(f"{score}\n")

def update_high_scores(new_score):
    global high_scores
    high_scores.append(new_score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10]  # Keep only top 10 scores
    save_high_scores()

def get_rank(score):
    return next((i + 1 for i, s in enumerate(high_scores) if score > s), len(high_scores) + 1)

def create_enemies():
    enemies.clear()
    rows = min(3 + current_level, 7)
    cols = min(6 + current_level, 12)
    
    patterns = [
        lambda i, j: (j * (WIDTH // cols), i * 50),  # Grid pattern
        lambda i, j: (WIDTH // 2 + (j - cols // 2) * 60, i * 50),  # V-shape pattern
        lambda i, j: (WIDTH // 2 + math.cos(i * math.pi / 3) * 200, 100 + math.sin(j * math.pi / 3) * 150),  # Circular pattern
        lambda i, j: (random.randint(0, WIDTH - enemy_width), random.randint(-200, 0)),  # Random pattern
    ]
    
    pattern = patterns[current_level % len(patterns)]
    
    for i in range(rows):
        for j in range(cols):
            x, y = pattern(i, j)
            enemy = {
                'x': x,
                'y': y,
                'speed': random.uniform(0.5, 1 + current_level * 0.2),
                'angle': random.uniform(0, 2 * math.pi),
                'radius': random.randint(50, 150),
                'center_x': x,
                'center_y': y,
                'descent_speed': random.uniform(0.2, 0.5 + current_level * 0.1),
                'points': random.randint(10, 30) * current_level
            }
            enemies.append(enemy)

def spawn_special_ship():
    pass
    # global special_ship
    # special_ship = {
    #     'x': random.choice([-60, WIDTH]),
    #     'y': random.randint(50, HEIGHT // 2),
    #     'speed': 2 if special_ship['x'] == -60 else -2,
    #     'radius': 30
    # }

def reset_game():
    global player_x, player_y, player_lives, game_over, level_complete, current_level, score, special_ship, special_ship_spawn_timer, player_shoot_angle
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    player_lives = 3
    game_over = False
    level_complete = False
    current_level = 1
    score = 0
    special_ship = None
    special_ship_spawn_timer = 0
    player_shoot_angle = 0
    player_bullets.clear()
    enemy_bullets.clear()
    create_enemies()

def start_next_level():
    global current_level, level_complete, special_ship_spawn_timer
    current_level += 1
    level_complete = False
    special_ship_spawn_timer = 0
    player_bullets.clear()
    enemy_bullets.clear()
    create_enemies()

def enemy_shoot(enemy, player_x, player_y):
    bullet_x = enemy['x'] + enemy_width // 2 - bullet_width // 2
    bullet_y = enemy['y'] + enemy_height

    if random.random() < 0.3:  # 30% chance to shoot at player
        dx = player_x + player_width // 2 - bullet_x
        dy = player_y - bullet_y
        distance = math.sqrt(dx**2 + dy**2)
        speed_x = bullet_speed * dx / distance
        speed_y = bullet_speed * dy / distance
    else:  # 70% chance to shoot straight down
        speed_x = 0
        speed_y = bullet_speed

    enemy_shoot_sound.play()  # Play enemy shoot sound
    return {
        'x': bullet_x,
        'y': bullet_y,
        'speed_x': speed_x,
        'speed_y': speed_y
    }

create_enemies()
load_high_scores()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game_over and not level_complete:
                bullet = {
                    'x': player_x + player_width // 2,
                    'y': player_y,
                    'angle': player_shoot_angle
                }
                player_bullets.append(bullet)
                player_shoot_sound.play()
            elif event.key == pygame.K_z and (game_over or level_complete):
                if game_over:
                    update_high_scores(score)
                    reset_game()
                else:
                    start_next_level()
  

    if not game_over and not level_complete:
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                player_shoot_angle = max(player_shoot_angle - 2, -60)  # Decrease angle, min -60 degrees
        
        if keys[pygame.K_RIGHT]:
                player_shoot_angle = min(player_shoot_angle + 2, 60)  # Increase angle, max 60 degrees

        if keys[pygame.K_z] and player_x > 0:
            player_x -= player_speed
        
        if keys[pygame.K_x] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Move enemies
        for enemy in enemies:
            enemy['angle'] += enemy['speed'] * 0.05
            enemy['x'] = enemy['center_x'] + math.cos(enemy['angle']) * enemy['radius']
            enemy['y'] = enemy['center_y'] + math.sin(enemy['angle']) * enemy['radius']
            
            # Gradual descent
            enemy['center_y'] += enemy['descent_speed']
            
            # Wrap around if enemy goes off-screen
            if enemy['y'] > HEIGHT:
                enemy['y'] = -enemy_height
                enemy['center_y'] = -enemy_height

            # Enemy shooting
            shoot_frequency = 200 - min(150, current_level * 10 + (50 - len(enemies)))
            if random.randint(1, max(shoot_frequency, 10)) == 1:
                enemy_bullets.append(enemy_shoot(enemy, player_x, player_y))

        # Move and check special ship
        if special_ship:
            special_ship['x'] += special_ship['speed']
            if (special_ship['x'] < -60 and special_ship['speed'] < 0) or (special_ship['x'] > WIDTH and special_ship['speed'] > 0):
                special_ship = None
        else:
            special_ship_spawn_timer += 1
            if special_ship_spawn_timer >= SPECIAL_SHIP_SPAWN_INTERVAL:
                spawn_special_ship()
                special_ship_spawn_timer = 0

        # Move bullets
        for bullet in player_bullets[:]:
            bullet['x'] += bullet_speed * math.sin(math.radians(bullet['angle']))
            bullet['y'] -= bullet_speed * math.cos(math.radians(bullet['angle']))
            if bullet['y'] < 0 or bullet['x'] < 0 or bullet['x'] > WIDTH:
                player_bullets.remove(bullet)

        for bullet in enemy_bullets[:]:
            bullet['x'] += bullet['speed_x']
            bullet['y'] += bullet['speed_y']
            if bullet['y'] > HEIGHT or bullet['x'] < 0 or bullet['x'] > WIDTH:
                enemy_bullets.remove(bullet)

        # Check for collisions
        for enemy in enemies[:]:
            for bullet in player_bullets[:]:
                if (enemy['x'] < bullet['x'] < enemy['x'] + enemy_width and
                    enemy['y'] < bullet['y'] < enemy['y'] + enemy_height):
                    score += enemy['points']
                    enemies.remove(enemy)
                    player_bullets.remove(bullet)
                    enemy_hit_sound.play()
                    break

        # Check for special ship collision
        # if special_ship:
        #     for bullet in player_bullets[:]:
        #         if (special_ship['x'] < bullet['x'] < special_ship['x'] + 60 and
        #             special_ship['y'] < bullet['y'] < special_ship['y'] + 60):
        #             player_lives += 1
        #             extra_life_sound.play()
        #             special_ship = None
        #             player_bullets.remove(bullet)
        #             break

        # Check for player hit
        for bullet in enemy_bullets[:]:
            if (player_x < bullet['x'] < player_x + player_width and
                player_y < bullet['y'] < player_y + player_height):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                player_hit_sound.play()
                if player_lives <= 0:
                    game_over = True
                break

        # Check for level complete
        if len(enemies) == 0:
            level_complete = True

    # Draw everything
    screen.fill(BLACK)
    screen.blit(player_img, (player_x, player_y))
    
    # Draw direction indicator line
    line_length = 20
    end_x = player_x + player_width // 2 + line_length * math.sin(math.radians(player_shoot_angle))
    end_y = player_y - line_length * math.cos(math.radians(player_shoot_angle))
    pygame.draw.line(screen, RED, (player_x + player_width // 2, player_y), (end_x, end_y), 2)

    for enemy in enemies:
        screen.blit(enemy_img, (enemy['x'], enemy['y']))
    if special_ship:
        screen.blit(special_ship_img, (special_ship['x'], special_ship['y']))
    for bullet in player_bullets:
        pygame.draw.rect(screen, WHITE, (bullet['x'], bullet['y'], bullet_width, bullet_height))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, YELLOW, (bullet['x'], bullet['y'], bullet_width, bullet_height))

    # Draw lives, level, and score
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    if game_over:
        rank = get_rank(score)
        game_over_text = font.render(f"Game Over! Final Score: {score}. Rank: {rank}. Press 'z' to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    elif level_complete:
        level_complete_text = font.render(f"Level Complete! Score: {score}. Press 'z' for next level", True, WHITE)
        screen.blit(level_complete_text, (WIDTH // 2 - level_complete_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()