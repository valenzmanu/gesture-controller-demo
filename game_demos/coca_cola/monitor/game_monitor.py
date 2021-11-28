import pygame.sprite

from game_demos.coca_cola.controlled_objects.controlled_object import ControlledObject
from game_demos.coca_cola.moving_objects.moving_objects import MovingObject


class GameMonitor:

    def __init__(self):
        self.score = 0

    @staticmethod
    def monitor_moving_objects(moving_object: MovingObject, moving_plane_size: tuple) -> None:
        width, height = moving_plane_size
        if moving_object.rect.left < 0.0 or moving_object.rect.left > width:
            moving_object.reset()
        if moving_object.rect.top < 0.0 or moving_object.rect.bottom > height:
            moving_object.reset()

    @staticmethod
    def check_collision(controlled_object: ControlledObject, moving_object: MovingObject) -> bool:
        collision = pygame.Rect.colliderect(controlled_object.rect, moving_object.rect)
        if collision:
            moving_object.reset()
        return collision

    def keep_score_count(self, collision: bool) -> None:
        if collision:
            self.score += 1
            print("Current score: %s" % self.score)
