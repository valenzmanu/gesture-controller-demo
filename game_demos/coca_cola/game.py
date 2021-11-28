import sys
import time

import pygame

from game_demos.coca_cola.controlled_objects.controlled_object import ControlledObject
from game_demos.coca_cola.controllers.hand_controller import HandController
from game_demos.coca_cola.moving_objects.moving_object_factory import MovingObjectFactory

pygame.init()

size = width, height = 1280, 720
black = 0, 0, 0

screen = pygame.display.set_mode(size)
background = pygame.image.load('images/background.jpg').convert()
background = pygame.transform.scale(background, size)
screen.blit(background, [0, 0])

bottles1 = MovingObjectFactory.make(quantity=7, image_filename='images/bottle1.png', random_speed=True,
                                    resize_factor=0.1, sparse_distance=200, speed_limits=(2, 5),
                                    initial_position=[10, 10])
bottles2 = MovingObjectFactory.make(quantity=6, image_filename='images/bottle2.png', random_speed=True,
                                    resize_factor=0.15, sparse_distance=200, speed_limits=(1, 4),
                                    initial_position=[100, 10])
glasses = MovingObjectFactory.make(quantity=5, image_filename='images/glass1.png', random_speed=True,
                                   resize_factor=0.15, sparse_distance=200, speed_limits=(3, 7),
                                   initial_position=[250, 10])
bottles = bottles1 + bottles2 + glasses

santa_bag = ControlledObject(image_filename='images/santa_bag.png',
                             resize_factor=0.1, initial_position=[50, 450])

hand_controller = HandController()
hand_controller.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hand_controller.stop()
            sys.exit()

    screen.blit(background, [0, 0])
    bag_position = hand_controller.get_mapped_coordinates((1280, 720))
    santa_bag.move_to(new_position=[bag_position[0], 450])
    screen.blit(santa_bag.image, santa_bag.rect)
    for bottle in bottles:
        bottle.move()
        time.sleep(0.00005)
        if bottle.rect.left < 0.0 or bottle.rect.left > width:
            bottle.reset()
        if bottle.rect.top < 0.0 or bottle.rect.bottom > height:
            bottle.reset()
        screen.blit(bottle.image, bottle.rect)

    pygame.display.flip()
