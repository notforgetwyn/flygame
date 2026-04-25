import arcade
from src.constants import *


class Player(arcade.Sprite):
    def __init__(self):
        texture = arcade.make_soft_square_texture(40, PLAYER_COLOR, 255, 255, 255)
        super().__init__(texture)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 100
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH

    def move(self, dx, dy):
        self.center_x += dx * self.speed
        self.center_y += dy * self.speed
        self.center_x = max(20, min(SCREEN_WIDTH - 20, self.center_x))
        self.center_y = max(20, min(SCREEN_HEIGHT - 20, self.center_y))

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def reset(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 100
        self.health = PLAYER_MAX_HEALTH