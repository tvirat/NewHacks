import pytest
import pygame
from unittest.mock import patch
from player import Player

@pytest.fixture
def player():
    pygame.init()
    image = pygame.Surface((50, 50))
    player_instance = Player(image, (100, 100))
    yield player_instance
    pygame.quit()

def test_player_initialization(player):
    assert player.rect.midbottom == (100, 100)
    assert player.speed == 200
    assert player.image.get_size() == (50, 50)

@patch('pygame.key.get_pressed')
def test_player_move_left(mock_get_pressed, player):
    initial_x = player.rect.x
    keys = [False] * 323  # pygame has 323 key constants
    keys[pygame.K_a] = True
    mock_get_pressed.return_value = keys
    player.movement_behavior.move(player, player.speed, 1)
    assert player.rect.x == initial_x - player.speed

@patch('pygame.key.get_pressed')
def test_player_move_right(mock_get_pressed, player):
    initial_x = player.rect.x
    keys = [False] * 323
    keys[pygame.K_d] = True
    mock_get_pressed.return_value = keys
    player.movement_behavior.move(player, player.speed, 1)
    assert player.rect.x == initial_x + player.speed

@patch('pygame.key.get_pressed')
def test_player_jump(mock_get_pressed, player):
    initial_y = player.rect.y
    keys = [False] * 323
    keys[pygame.K_SPACE] = True
    mock_get_pressed.return_value = keys
    player.movement_behavior.jump(player, 1)
    assert player.rect.y < initial_y