# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Import Statements ---------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
import random
from jump import handle_jump, is_jumping, velocity_y, jump_height, gravity
import backdrop

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Global Variable Declaration -----------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# List to hold coin positions
coins = []

# Colors
button_bg = (2, 73, 91)
button_text = (241, 250, 251)

# List to hold obstacle positions
obstacles = []
slimes = []

# Player's lives
lives = 3

# High score
high_score = 0  # Initialize high score

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Start Screen --------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# Initiate the Start window

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Font
font = pygame.font.SysFont(None, 48)

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Load Pictures -------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# Load and scale the start screen background image
start_background = pygame.image.load('start_background.png').convert()
start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))

# Load and scale the obstacle image
obstacle_image = pygame.image.load('obstacle.png').convert_alpha()  # Ensure transparency
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Adjust size as needed

# Load and scale the slime image
slime_image = pygame.image.load('slime.png').convert_alpha()  # Ensure transparency
slime_image = pygame.transform.scale(slime_image, (50, 50))  # Adjust size as needed

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Global Functions ----------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# Function to calculate and display the number of lives left 
def draw_lives(surface, x, y, lives):
    for i in range(lives):
        surface.blit(heart_image, (x - 40 * i, y))

# Function to calculate and display the number of lives left 
def draw_score(surface, score, x, y):
    score_text = font.render(f'Score: {score}', True, button_text)
    surface.blit(score_text, (x, y))

# Functions for buttons
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to draw rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# start_screen function
def start_screen():
    click = False
    while True:
        screen.blit(start_background, (0, 0))
        title_text = 'Your Game Title'  # Replace with your actual game title
        title_font = pygame.font.SysFont(None, 72)  # Larger font for the title
        draw_text(title_text, title_font, button_bg, screen, WIDTH // 2 - title_font.size(title_text)[0] // 2, HEIGHT // 2 - title_font.size(title_text)[1] - 100)
        draw_text('High Score: {}'.format(high_score), font, button_bg, screen, 10, 10)

        mx, my = pygame.mouse.get_pos()

        button_start = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50)
        button_exit = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)

        if button_start.collidepoint((mx, my)):
            if click:
                return
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        # Draw rounded rectangles for start and exit buttons
        draw_rounded_rect(screen, button_bg, button_start, 10)
        draw_rounded_rect(screen, button_bg, button_exit, 10)

        draw_text('Start', font, button_text, screen, button_start.centerx - font.size('Start')[0] // 2, button_start.centery - font.size('Start')[1] // 2)
        draw_text('Exit', font, button_text, screen, button_exit.centerx - font.size('Exit')[0] // 2, button_exit.centery - font.size('Exit')[1] // 2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)

start_screen()

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Main Game Screen ----------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------


# Initiate the main game screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load the default font
font = pygame.font.SysFont(None, 24)

# Load and scale the heart image
heart_image = pygame.image.load('heart.webp').convert_alpha()  # Ensure transparency
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust size as needed

# Load and scale the background image
background = pygame.image.load('backdrop.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Load and scale the monster image
monster = pygame.image.load('monster.png').convert_alpha()  # Ensure transparency
monster = pygame.transform.scale(monster, (monster.get_width() // 7, monster.get_height() // 7))
monster_rect = monster.get_rect()
monster_rect.center = (24, HEIGHT - 100)  # Start position

# Load and scale the coin image
coin_image = pygame.image.load('coin.png').convert_alpha()  # Ensure transparency
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Adjust size as needed

# Initial background position
background_x = 0

# Speed of the monster and background
monster_speed = 1
background_speed = 20

# Player's score
score = 0

# Main Game loop/function
def main_game_loop(background_x, coins, obstacles, slimes, screen, lives, score):
    # Initialize/reset variables here
    monster_rect.center = (24, HEIGHT - 135)  # Reset player position
    coins.clear()  # Clear coins list
    obstacles.clear() 
    slimes.clear() 
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop
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
        
        # Adjust monster_rect.y before handling jump to ensure it starts from the correct height
        if monster_rect.bottom > HEIGHT - 100:
            monster_rect.bottom = HEIGHT - 100
        
        handle_jump(monster_rect, dt)  # Call handle_jump to manage jumping

        # Define jump height and minimum height
        max_jump_height = 150  # Adjust according to jump capabilities
        min_height = HEIGHT - 135

        # Generate coins randomly
        if random.randint(0, 100) < 5:  # Adjust probability as needed
            coin_x = random.randint(0, WIDTH - 30)
            coin_y = random.randint(min_height - max_jump_height, min_height)  # Restrict y-coordinate within jump range
            coins.append(pygame.Rect(coin_x, coin_y, 30, 30))

        # Generate obstacles randomly
        if random.randint(0, 100) < 4:  # Adjust probability as needed
            obstacle_x = random.randint(0, WIDTH - 50)
            obstacle_y = random.randint(min_height - max_jump_height, min_height)
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, 50, 50))

        # Generate slimes randomly
        if random.randint(0, 100) < 4:  # Adjust probability as needed
            slime_x = random.randint(0, WIDTH - 50)
            slime_y = min_height + 50
            slimes.append(pygame.Rect(slime_x, slime_y, 50, 50))

        # To ensure seamless scrolling
        if background_x >= WIDTH:
            background_x = 0
        elif background_x <= -WIDTH:
            background_x = 0

        # Check for collisions between monster and coins
        for coin in coins[:]:
            if monster_rect.colliderect(coin):
                coins.remove(coin)
                score += 1  # Increase score

        # Check for collisions between monster and obstacles
        for obstacle in obstacles[:]:
            if monster_rect.colliderect(obstacle):
                obstacles.remove(obstacle)
                lives -= 1  # Decrease lives
                if lives == 0:
                    running = False  # Game over if no lives left
        
        # Check for collisions between monster and slimes
        for slime in slimes[:]:
            if monster_rect.colliderect(slime):
                obstacles.remove(slime)
                lives -= 1  # Decrease lives
                if lives == 0:
                    running = False  # Game over if no lives left


        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x - WIDTH, 0))
        screen.blit(background, (background_x + WIDTH, 0))
        screen.blit(monster, monster_rect.topleft)

        # Draw lives counter
        draw_text('Lives Left:', font, button_text, screen, WIDTH - 198, 13.5)
        draw_lives(screen, WIDTH - 32, 6.5, lives)

        # Draw scores counter
        draw_score(screen, score, 10, 10)
        for coin in coins:
            screen.blit(coin_image, coin.topleft)
        for obstacle in obstacles:
            screen.blit(obstacle_image, obstacle.topleft)
        for slime in slimes:
            screen.blit(slime_image, slime.topleft)

        pygame.display.flip()
        clock.tick(FPS)

main_game_loop(background_x, coins, obstacles, [], screen, lives, score)

# Print the score after quitting the game
print(f"Score: {score}")

# Print the result after quitting the game
print(f"Lives remaining: {lives}")

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Game End Screen -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

click = False  # Ensure click is defined globally

def end_screen(final_score):  # Remove total_time parameter
    global click  # Use global click to ensure it's recognized
    while True:
        screen.blit(start_background, (0, 0))  # Use the start screen background
        draw_text(f'Final Score: {final_score}', font, button_text, screen, WIDTH // 2 - 100, HEIGHT // 2 - 100)
        mx, my = pygame.mouse.get_pos()
        button_play_again = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
        if button_play_again.collidepoint((mx, my)):
            if click:
                main_game_loop(background_x, coins, obstacles, slimes, screen, 3, 0)  # Restart the game
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        draw_rounded_rect(screen, button_bg, button_play_again, 10)
        draw_rounded_rect(screen, button_bg, button_exit, 10)
        draw_text('Play Again', font, button_text, screen, button_play_again.centerx - font.size('Play Again')[0] // 2, button_play_again.centery - font.size('Play Again')[1] // 2)
        draw_text('Exit', font, button_text, screen, button_exit.centerx - font.size('Exit')[0] // 2, button_exit.centery - font.size('Exit')[1] // 2)
        click = False  # Reset click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(FPS)

# Replace the earlier end_screen call with this updated one
end_screen(score)  # Call end_screen with only the final score parameter
