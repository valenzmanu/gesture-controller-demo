import sys
import time

import pygame

from game_demos.coca_cola.controlled_objects.controlled_object import ControlledObject
from game_demos.coca_cola.controllers.hand_controller import HandController
from game_demos.coca_cola.monitor.game_monitor import GameMonitor
from game_demos.coca_cola.moving_objects.moving_object_factory import MovingObjectFactory

pygame.init()
pygame.display.set_caption('Pantalla')
icon = pygame.image.load('images/coca_cola_icon.png')
pygame.display.set_icon(icon)

WINDOW_SIZE = width, height = 1280, 720
GAME_WINDOW_SIZE = game_width, game_height = 854, 720
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)

# Screen Indicators and Images
screen = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.image.load('images/background.jpg').convert()
background = pygame.transform.scale(background, GAME_WINDOW_SIZE)
screen.blit(background, [426, 0])
font = pygame.font.Font('freesansbold.ttf', 32)
santa_image = pygame.image.load('images/santa_photo.jfif')
santa_image = pygame.transform.scale(santa_image, [426, 720])
santa_image_rect = santa_image.get_rect()
screen.blit(santa_image, santa_image_rect)

# Game Objects
bottles1 = MovingObjectFactory.make(quantity=7, image_filename='images/bottle1.png', random_speed=True,
                                    resize_factor=0.1, sparse_distance=200, speed_limits=(2, 5),
                                    initial_position=[436, 5])
bottles2 = MovingObjectFactory.make(quantity=6, image_filename='images/bottle2.png', random_speed=True,
                                    resize_factor=0.15, sparse_distance=200, speed_limits=(1, 4),
                                    initial_position=[436 + 100, 5])
glasses = MovingObjectFactory.make(quantity=5, image_filename='images/glass1.png', random_speed=True,
                                   resize_factor=0.15, sparse_distance=200, speed_limits=(3, 7),
                                   initial_position=[436 + 250, 5])
bottles = bottles1 + bottles2 + glasses

santa_bag = ControlledObject(image_filename='images/santa_bag.png',
                             resize_factor=0.1, initial_position=[50, 450])
# Game Monitor
game_monitor = GameMonitor()

# Game Controller
hand_controller = HandController(camera_index=1)
hand_controller.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hand_controller.stop()
            sys.exit()

    screen.blit(background, [426, 0])
    bag_position = hand_controller.get_mapped_coordinates(GAME_WINDOW_SIZE, offset=(426, 0))
    santa_bag.move_to(new_position=[bag_position[0], 450])
    screen.blit(santa_bag.image, santa_bag.rect)
    for bottle in bottles:
        bottle.move()
        time.sleep(0.00001)
        game_monitor.monitor_moving_objects(bottle, GAME_WINDOW_SIZE, mov_plane_offset=(426, 0))
        screen.blit(bottle.image, bottle.rect)
        collision = game_monitor.check_collision(santa_bag, bottle)
        score = game_monitor.keep_score_count(collision)
        score_text = text = font.render('Score: %s' % score, True, WHITE, RED)
        text_rect = text.get_rect()
        text_rect.center = (width - 100, 50)
        screen.blit(text, text_rect)
        screen.blit(santa_image, santa_image_rect)
    pygame.display.flip()
