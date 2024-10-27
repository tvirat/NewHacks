# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Import Statements ---------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
import random
from jump import handle_jump, is_jumping, velocity_y, jump_height, gravity
import pytmx
from pytmx import load_pygame

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
start_background = pygame.image.load('images/start_background.png').convert()
start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))

# Load and scale the obstacle image
obstacle_image = pygame.image.load('images/obstacle.png').convert_alpha()  # Ensure transparency
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Adjust size as needed

# Load and scale the slime image
slime_image = pygame.image.load('images/slime.png').convert_alpha()  # Ensure transparency
slime_image = pygame.transform.scale(slime_image, (50, 50))  # Adjust size as needed

class Terrain:
    def __init__(self, tmx_data):
        self.tmx_data = tmx_data
        self.collision_rects = []
        self.tiles = []  # Store all tiles with their types
        self.collision_types = {'terrain', 'tree', 'mushroom', 'platform'}
        self.load_tiles()
    
    def load_tiles(self):
        """Load all tiles and their properties"""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer.iter_data():
                    if gid:  # If there's a tile at this position
                        tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                        if tile_props:
                            # Convert tile coordinates to pixel coordinates
                            pixel_x = x * self.tmx_data.tilewidth
                            pixel_y = y * self.tmx_data.tileheight
                            # Create a rectangle for this tile
                            rect = pygame.Rect(
                                pixel_x, 
                                pixel_y, 
                                self.tmx_data.tilewidth, 
                                self.tmx_data.tileheight
                            )
                            
                            # Store tile data
                            tile_data = {
                                'rect': rect,
                                'type': tile_props.get('type', 'default'),
                                'gid': gid
                            }
                            
                            self.tiles.append(tile_data)
                            
                            # If it's a collision tile, add to collision_rects
                            if tile_props.get('type') in self.collision_types:
                                self.collision_rects.append(tile_data)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw all tiles with their actual images"""
        for tile in self.tiles:
            # Get the tile image from the tmx data
            tile_image = self.tmx_data.get_tile_image_by_gid(tile['gid'])
            if tile_image:
                # Adjust position for camera offset
                draw_x = tile['rect'].x - camera_offset[0]
                draw_y = tile['rect'].y - camera_offset[1]
                surface.blit(tile_image, (draw_x, draw_y))
    
    def get_slime_rects(self):
        """Return a list of rectangles for all slime tiles"""
        return [tile['rect'] for tile in self.tiles if tile['type'] == 'slime']
    
    def draw_dev(self, surface, camera_offset=(0, 0)):
        """Draw the terrain collision boxes (for debugging)"""
        colors = {
            'terrain': (255, 0, 0),    # Red for ground
            'tree': (0, 255, 0),      # Green for walls
            'platform': (0, 0, 255),  # Blue for platforms
            'solid': (255, 255, 0)    # Yellow for solid objects
        }
        
        for collision in self.collision_rects:
            rect = collision['rect'].copy()
            rect.x -= camera_offset[0]
            rect.y -= camera_offset[1]
            color = colors.get(collision['type'], (255, 255, 255))
            pygame.draw.rect(surface, color, rect, 1)
    
    def check_collision(self, player_rect, velocity_y=0):
        """Check collision between player and terrain"""
        collisions = {
            'top': False,
            'bottom': False,
            'left': False,
            'right': False,
            'type': None  # Initialize type as None by default
        }
        
        collision_found = False
        for collision in self.collision_rects:
            rect = collision['rect']
            
            if player_rect.colliderect(rect):
                collision_found = True
                # Store the type of the tile we're colliding with
                collisions['type'] = collision['type']
                
                # Calculate overlap
                overlap_x = min(player_rect.right - rect.left, rect.right - player_rect.left)
                overlap_y = min(player_rect.bottom - rect.top, rect.bottom - player_rect.top)
                
                # Resolve collision based on the smallest overlap
                if overlap_x < overlap_y:
                    if player_rect.centerx < rect.centerx:
                        player_rect.right = rect.left
                        collisions['right'] = True
                    else:
                        player_rect.left = rect.right
                        collisions['left'] = True
                else:
                    if player_rect.centery < rect.centery:
                        player_rect.bottom = rect.top
                        collisions['bottom'] = True
                    else:
                        player_rect.top = rect.bottom
                        collisions['top'] = True
        
        return collisions

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Adjust size as needed
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.jump_height = -20
        self.gravity = 0.8
        self.speed = 1  # Your monster_speed value
    
    def handle_movement(self, keys, terrain, dt):
        # Store old position for collision checking
        old_position = self.rect.copy()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Check horizontal collisions
        collisions = terrain.check_collision(self.rect, self.velocity_y)
        if collisions['left'] or collisions['right']:
            self.rect = old_position
        
        # Jump input
        if keys[pygame.K_UP] and self.on_ground and not self.is_jumping:
            self.is_jumping = True
            self.on_ground = False
            self.velocity_y = self.jump_height
        
        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Check vertical collisions
        collisions = terrain.check_collision(self.rect, self.velocity_y)
        
        # Handle collision responses
        if collisions['bottom']:
            self.rect.bottom = old_position.bottom
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0
            
            # Special collision handling for different tile types
            if collisions['type'] == 'mushroom':
                self.velocity_y = self.jump_height * 1.5  # Bigger bounce on mushrooms
                self.is_jumping = True
                self.on_ground = False
        
        if collisions['top']:
            self.rect.top = old_position.top
            self.velocity_y = 0
        
        # Prevent falling through the floor (backup check)
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0

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
heart_image = pygame.image.load('images/heart.webp').convert_alpha()  # Ensure transparency
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust size as needed

# Load and scale the background image
background = pygame.image.load('images/backdrop.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Load and scale the monster image
monster = pygame.image.load('images/monster.png').convert_alpha()  # Ensure transparency
monster = pygame.transform.scale(monster, (monster.get_width() // 7, monster.get_height() // 7))
monster_rect = monster.get_rect()
monster_rect.center = (24, HEIGHT - 100)  # Start position

# Load and scale the coin image
coin_image = pygame.image.load('images/coin.png').convert_alpha()  # Ensure transparency
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Adjust size as needed

# Initial background position
background_x = 0

# Speed of the monster and background
monster_speed = 1
background_speed = 20

# Player's score
score = 0

# Main Game loop/function
def main_game_loop(background_x, coins, obstacles, slimes, screen, lives, score, velocity_y):
    # Initialize/reset variables here
    player = Player(24, HEIGHT - 135)  
    coins.clear()  # Clear coins list
    obstacles.clear() 
    slimes.clear()
    # Create the terrain object
    tmx_data = load_pygame('assets/levels/first_level.tmx')
    terrain = Terrain(tmx_data) 
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        
        # Handle player movement
        player.handle_movement(keys, terrain, dt)
        
        # Handle background wrapping
        if background_x >= WIDTH:
            background_x = 0
        elif background_x <= -WIDTH:
            background_x = 0

        # Get slime positions from the terrain
        slime_rects = terrain.get_slime_rects()
        
        # Check for collisions with slimes
        for slime_rect in slime_rects:
            if player.rect.colliderect(slime_rect):
                lives -= 1
                if lives == 0:
                    running = False

        # Drawing
        screen.fill((0, 0, 0))
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x - WIDTH, 0))
        screen.blit(background, (background_x + WIDTH, 0))
        
        # Draw terrain collision boxes (optional, for debugging)
        #terrain.draw_dev(screen, (background_x, 0))
        
        #slime
        terrain.draw(screen, (background_x, 0))
        
        # Draw player (using your monster image)
        screen.blit(monster, player.rect.topleft)
        
        # Draw lives counter
        draw_text('Lives Left:', font, button_text, screen, WIDTH - 198, 13.5)
        draw_lives(screen, WIDTH - 32, 6.5, lives)

        # Draw scores counter
        draw_score(screen, score, 10, 10)
        for obstacle in obstacles:
            screen.blit(obstacle_image, obstacle.topleft)

        pygame.display.flip()
        clock.tick(FPS)

main_game_loop(background_x, coins, obstacles, [], screen, lives, score, velocity_y)

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
