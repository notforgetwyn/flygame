import arcade
from .enemy import Enemy
from ..constants import *


class EnemyFactory:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = ENEMY_SPAWN_INTERVAL

    def update(self, delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            return Enemy()
        return None

    def reset(self):
        self.spawn_timer = 0
