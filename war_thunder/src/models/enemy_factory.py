import random
from src.models.enemy import Enemy
from src.constants import *


class EnemyFactory:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = ENEMY_SPAWN_INTERVAL
        self.wave = 0
        self.enemies_in_wave = 0
        self.enemies_spawned = 0
        self.wave_break = False
        self.wave_break_timer = 0
        self.homing_count = 0
        self.side_count = 0

    def start_next_wave(self):
        self.wave += 1
        self.enemies_in_wave = 3 + self.wave * 2
        self.enemies_spawned = 0
        self.wave_break = False
        self.homing_count = min(self.wave - 1, 3) if self.wave > 1 else 0
        self.side_count = min(self.wave // 2, 2) if self.wave > 2 else 0

    def update(self, delta_time):
        if self.wave_break:
            self.wave_break_timer -= delta_time
            if self.wave_break_timer <= 0:
                self.start_next_wave()
            return None

        if self.enemies_spawned >= self.enemies_in_wave:
            self.wave_break = True
            self.wave_break_timer = 2
            return None

        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.enemies_spawned += 1
            return self._create_enemy()

        return None

    def _create_enemy(self):
        if self.wave >= 5 and self.enemies_spawned == 1 and self.wave % 5 == 0:
            return Enemy(Enemy.AI_BOSS)

        roll = random.random()
        if self.homing_count > 0 and roll < 0.3:
            self.homing_count -= 1
            return Enemy(Enemy.AI_HOMING)
        if self.side_count > 0 and roll < 0.5:
            self.side_count -= 1
            return Enemy(Enemy.AI_SIDE)
        return Enemy(Enemy.AI_NORMAL)

    def reset(self):
        self.spawn_timer = 0
        self.wave = 0
        self.enemies_in_wave = 0
        self.enemies_spawned = 0
        self.wave_break = False
        self.wave_break_timer = 0
