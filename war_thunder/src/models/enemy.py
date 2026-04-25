import arcade
import random
from ..constants import *


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = random.randint(30, SCREEN_WIDTH - 30)
        self.center_y = SCREEN_HEIGHT + 20
        self.width = 35
        self.height = 35
        self.speed = ENEMY_SPEED
        self.health = 1
        self.texture = arcade.make_soft_circle_texture(17, ENEMY_COLOR, 255, 255, 255)

    def update(self):
        self.center_y -= self.speed
        if self.center_y < -40:
            self.kill()
