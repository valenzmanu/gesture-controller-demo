from game_demos.coca_cola.moving_objects.moving_objects import MovingObject
import random


class MovingObjectFactory:

    def __init__(self):
        pass

    @staticmethod
    def make(quantity: int, image_filename: str, moving_plane_size: tuple = None, initial_speed: list = None,
             initial_position: list = None, sparse_distance: int = 50, resize_factor=0.25, random_speed=False,
             speed_limits=(1, 10)) -> list:
        objects = []
        for i in range(quantity):
            speed = [0, random.randint(speed_limits[0], speed_limits[1])] if random_speed else initial_speed
            if initial_position is not None:
                position = [i * sparse_distance + initial_position[0], initial_position[1]]
            else:
                position = [i * sparse_distance + 100, 10]
            objects.append(
                MovingObject(image_filename=image_filename,
                             moving_plane_size=moving_plane_size,
                             initial_speed=speed,
                             initial_position=position,
                             resize_factor=resize_factor
                             ))
        return objects
