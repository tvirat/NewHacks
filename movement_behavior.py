"""Using the Strategy pattern to implement movement behaviors for entities."""

import pygame

class MovementBehavior:
    """Abstract class representing a movement behavior."""

    def move(self, entity: pygame.sprite.Sprite, speed: float, dt: float):
        """Move the entity.

        Args:
            entity: The entity to move.
            speed: The speed at which to move the entity.
            dt: The time since the last frame.
        """
        raise NotImplementedError("move() must be implemented in a subclass.")

    def jump(self, entity, dt: float):
        """Make the entity jump."""
        raise NotImplementedError("jump() must be implemented in a subclass.")


class PlayerMovementBehavior(MovementBehavior):
    """A class to represent the player's movement behavior."""

    def move(self, entity: pygame.sprite.Sprite, speed: float, dt: float):
        """Get player input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            entity.rect.x -= speed * dt
        if keys[pygame.K_d]:
            entity.rect.x += speed * dt
        if keys[pygame.K_SPACE]:
            self.jump(entity, dt)

    def jump(self, entity: pygame.sprite.Sprite, dt: float):
        """Make the player jump."""
        jump_factor = 3
        entity.rect.y -= jump_factor * entity.rect.height * dt