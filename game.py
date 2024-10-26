import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load and scale the background image
background = pygame.image.load('background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Load and scale the monster image
monster = pygame.image.load('monster.png').convert_alpha()  # Ensure transparency
monster = pygame.transform.scale(monster, (monster.get_width() // 7, monster.get_height() // 7))
monster_rect = monster.get_rect()
monster_rect.center = (WIDTH // 2, HEIGHT // 2)  # Start position

# Initial background position
background_x = 0

# Speed of the monster and background
monster_speed = 1
background_speed = 20

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        monster_rect.x -= monster_speed  # Move monster left
        background_x += background_speed  # Move background right
    if keys[pygame.K_RIGHT]:
        monster_rect.x += monster_speed  # Move monster right
        background_x -= background_speed  # Move background left

    # To ensure seamless scrolling
    if background_x >= WIDTH:
        background_x = 0
    elif background_x <= -WIDTH:
        background_x = 0

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x - WIDTH, 0))
    screen.blit(background, (background_x + WIDTH, 0))
    screen.blit(monster, monster_rect.topleft)
    pygame.display.flip()

    clock.tick(FPS)

# Quit pygame
pygame.quit()
