import arcade
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PowerUp:
    TYPE_BULLET = 'bullet'
    TYPE_SHIELD = 'shield'
    TYPE_BOMB = 'bomb'

    def __init__(self, x, y, power_type):
        self.center_x = x
        self.center_y = y
        self.width = 20
        self.height = 20
        self.power_type = power_type
        self.speed = 2
        self.active = True
        self.duration = 0

        colors = {
            self.TYPE_BULLET: arcade.color.YELLOW,
            self.TYPE_SHIELD: arcade.color.BLUE,
            self.TYPE_BOMB: arcade.color.RED
        }
        self.color = colors.get(power_type, arcade.color.WHITE)

    def update(self):
        self.center_y -= self.speed
        if self.center_y < -20:
            self.active = False

    def draw(self):
        if self.power_type == self.TYPE_BULLET:
            self.draw_bullet_powerup()
        elif self.power_type == self.TYPE_SHIELD:
            self.draw_shield_powerup()
        elif self.power_type == self.TYPE_BOMB:
            self.draw_bomb_powerup()

    def draw_bullet_powerup(self):
        x, y = self.center_x, self.center_y
        arcade.draw_star(x, y, 12, 5, arcade.color.YELLOW)
        arcade.draw_text('★', x - 8, y - 10, arcade.color.YELLOW, 20)

    def draw_shield_powerup(self):
        x, y = self.center_x, self.center_y
        arcade.draw_ellipse_filled(x, y, 16, 20, arcade.color.BLUE)
        arcade.draw_ellipse_outline(x, y, 16, 20, arcade.color.WHITE, 2)

    def draw_bomb_powerup(self):
        x, y = self.center_x, self.center_y
        arcade.draw_circle_filled(x, y, 10, arcade.color.RED)
        arcade.draw_line(x - 10, y + 5, x + 10, y + 5, arcade.color.ORANGE, 3)
        arcade.draw_line(x, y + 10, x, y + 15, arcade.color.ORANGE, 2)

    def get_rect(self):
        from arcade import Rect
        return Rect(self.center_x - 10, self.center_y - 10, 20, 20)
