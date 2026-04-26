import arcade
import random
import math
from src.constants import *


class Enemy(arcade.Sprite):
    AI_NORMAL = 'normal'
    AI_HOMING = 'homing'
    AI_SIDE = 'side'
    AI_BOSS = 'boss'

    def __init__(self, ai_type=AI_NORMAL):
        self.ai_type = ai_type
        self.bullet_cooldown = 0
        self.target_y = SCREEN_HEIGHT - 100

        if ai_type == self.AI_BOSS:
            super().__init__()
            self.center_x = SCREEN_WIDTH // 2
            self.center_y = SCREEN_HEIGHT + 50
            self.speed = BOSS_SPEED
            self.health = BOSS_HEALTH
            self.width = BOSS_WIDTH
            self.height = BOSS_HEIGHT
        else:
            texture = arcade.make_soft_circle_texture(17, ENEMY_COLOR, 255, 255, 255)
            super().__init__(texture)
            self.center_x = random.randint(30, SCREEN_WIDTH - 30)
            self.center_y = SCREEN_HEIGHT + 20
            self.speed = ENEMY_SPEED
            self.health = 1

        self.side_direction = random.choice([-1, 1]) if ai_type == self.AI_SIDE else 0

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def can_shoot(self):
        return self.ai_type == self.AI_BOSS and self.bullet_cooldown <= 0

    def shoot(self):
        self.bullet_cooldown = ENEMY_BULLET_COOLDOWN
        return EnemyBullet(self.center_x, self.center_y - 25)

    def update(self, delta_time=None):
        if self.ai_type == self.AI_HOMING:
            self.update_homing()
        elif self.ai_type == self.AI_SIDE:
            self.update_side()
        elif self.ai_type == self.AI_BOSS:
            self.update_boss()
        else:
            self.update_normal()

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= delta_time if delta_time else 1/60

        if self.center_y < -60:
            self.kill()

    def update_normal(self):
        self.center_y -= self.speed

    def update_homing(self):
        if self.center_y > 100:
            self.center_y -= self.speed * 0.7
        else:
            dx = SCREEN_WIDTH // 2 - self.center_x
            self.center_x += dx * 0.02
            self.center_y -= self.speed * 0.5

    def update_side(self):
        self.center_y -= self.speed * 0.8
        self.center_x += self.side_direction * self.speed * 0.6
        if self.center_x < 30 or self.center_x > SCREEN_WIDTH - 30:
            self.side_direction *= -1

    def update_boss(self):
        if self.center_y > SCREEN_HEIGHT - 120:
            self.center_y -= self.speed
        else:
            dx = SCREEN_WIDTH // 2 - self.center_x
            self.center_x += dx * 0.015
            if abs(dx) < 5:
                self.center_x = SCREEN_WIDTH // 2

    def draw(self):
        if self.ai_type == self.AI_BOSS:
            x, y = self.center_x, self.center_y
            arcade.draw_polygon_filled([
                (x, y - 25), (x - 30, y + 15), (x - 15, y + 5),
                (x + 15, y + 5), (x + 30, y + 15)
            ], arcade.color.RED)
            arcade.draw_polygon_filled([
                (x - 30, y + 5), (x - 40, y + 15), (x - 25, y + 20)
            ], arcade.color.RED)
            arcade.draw_polygon_filled([
                (x + 30, y + 5), (x + 40, y + 15), (x + 25, y + 20)
            ], arcade.color.RED)
        else:
            super().draw()


class EnemyBullet(arcade.Sprite):
    def __init__(self, x, y):
        texture = arcade.make_soft_circle_texture(6, arcade.color.ORANGE, 255, 255, 255)
        super().__init__(texture)
        self.center_x = x
        self.center_y = y
        self.speed = ENEMY_BULLET_SPEED

    def update(self, delta_time=None):
        self.center_y -= self.speed
        if self.center_y < -20:
            self.kill()
