import pygame

from movement_behavior import PlayerMovementBehavior

class Player(pygame.sprite.Sprite):
    """A class to represent the player."""

    image: pygame.Surface
    rect: pygame.FRect
    movement_behavior: PlayerMovementBehavior
    speed: float

    def __init__(self, image: pygame.Surface, midbottom: tuple[float, float]) -> None:
        """Initialize the player with the given image and set its starting midbottom
        position."""
        super().__init__()
        self.image = image
        self.image.fill("red")  # Temporary
        self.movement_behavior = PlayerMovementBehavior()
        self.rect = self.image.get_frect()
        self.rect.midbottom = midbottom
        self.speed = 200


    def update(self, dt):
        """Update player position."""
        self.movement_behavior.move(self, self.speed, dt)
