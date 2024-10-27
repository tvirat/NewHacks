import pygame
from settings import HEIGHT

# Add these variables
is_jumping = False
velocity_y = 0
jump_height = -15
gravity = 0.8

def handle_jump(monster_rect, dt):
    global is_jumping, velocity_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        velocity_y = jump_height
    # Apply gravity
    if is_jumping:
        velocity_y += gravity
        monster_rect.y += velocity_y
        if monster_rect.bottom >= HEIGHT - 100:  # Ensure player doesn't fall below the minimum height
            monster_rect.bottom = HEIGHT - 100
            is_jumping = False
            velocity_y = 0


