import arcade
from ..constants import *


class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 6
        self.height = 15
        self.speed = BULLET_SPEED
        self.texture = arcade.make_color_square_texture(6, 15, BULLET_COLOR)

    def update(self):
        self.center_y += self.speed
        if self.center_y > SCREEN_HEIGHT + 10:
            self.kill()
