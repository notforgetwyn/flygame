import arcade
from src.constants import *


class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        texture = arcade.make_color_square_texture(6, 15, BULLET_COLOR)
        super().__init__(texture)
        self.center_x = x
        self.center_y = y
        self.speed = BULLET_SPEED

    def update(self, delta_time=None):
        self.center_y += self.speed
        if self.center_y > SCREEN_HEIGHT + 10:
            self.kill()