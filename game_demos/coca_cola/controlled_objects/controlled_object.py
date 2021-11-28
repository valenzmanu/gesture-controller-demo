import pygame


class ControlledObject:

    def __init__(self, image_filename: str, moving_plane_size: tuple = None, resize_factor=0.25,
                 initial_position: list = None):
        image = pygame.image.load(image_filename)
        image_size = image.get_size()
        self.filename = image_filename
        self.moving_plane_size = moving_plane_size
        self.image = self._resize_image(image, image_size, resize_factor)
        self.speed = [0, 0]
        rect = self.image.get_rect()
        if initial_position is not None and len(initial_position) == 2:
            rect.left = initial_position[0]
            rect.top = initial_position[1]
        self.rect = rect

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        message = "filename: %s, speed: %s, rect: [%s, %s, %s, %s]" % (
            self.filename, self.speed, self.rect.top, self.rect.bottom, self.rect.right, self.rect.left)
        return message

    @staticmethod
    def _resize_image(image, image_size, resize_factor):
        x, y = image_size
        new_size = (resize_factor * x, resize_factor * y)
        return pygame.transform.scale(image, new_size)

    def move_to(self, new_position: list) -> list:
        self.rect.left = new_position[0]
        self.rect.top = new_position[1]
        return self.rect
