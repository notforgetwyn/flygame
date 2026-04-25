import arcade
import random
from src.constants import *


class Enemy(arcade.Sprite):
    def __init__(self):
        texture = arcade.make_soft_circle_texture(17, ENEMY_COLOR, 255, 255, 255)
        super().__init__(texture)
        self.center_x = random.randint(30, SCREEN_WIDTH - 30)
        self.center_y = SCREEN_HEIGHT + 20
        self.speed = ENEMY_SPEED

    def update(self, delta_time=None):
        self.center_y -= self.speed
        if self.center_y < -40:
            self.kill()