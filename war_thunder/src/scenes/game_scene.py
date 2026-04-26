import arcade
import random
from src.constants import *
from src.models.enemy import Enemy, EnemyBullet
from src.models.enemy_factory import EnemyFactory
from src.models.powerup import PowerUp
from src.models.powerup_factory import PowerUpFactory
from src.models.explosion import Explosion
from src.core.save_service import SaveService
from src.core.settings_service import SettingsService
from src.core.sound_service import SoundService


class Bullet:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.width = 6
        self.height = 15
        self.speed = BULLET_SPEED
        self.active = True

    def update(self, delta_time=None):
        self.center_y += self.speed
        if self.center_y > SCREEN_HEIGHT + 10:
            self.active = False

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(self.center_x - 3, self.center_y - 8, 6, 16, arcade.color.YELLOW)


class Player:
    def __init__(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 100
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.shield = 0
        self.bullet_level = 1

    def move(self, dx, dy):
        self.center_x += dx * self.speed
        self.center_y += dy * self.speed
        self.center_x = max(20, min(SCREEN_WIDTH - 20, self.center_x))
        self.center_y = max(20, min(SCREEN_HEIGHT - 20, self.center_y))

    def take_damage(self):
        if self.shield > 0:
            self.shield -= 1
            return False
        self.health -= 1
        return self.health <= 0

    def reset(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 100
        self.health = PLAYER_MAX_HEALTH
        self.shield = 0
        self.bullet_level = 1


class GameScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.hit_flash = 0
        self.powerup_message = ''
        self.powerup_timer = 0

        self.player = None
        self.bullet_list = []
        self.enemy_list = None
        self.enemy_factory = None
        self.powerup_list = []
        self.bullet_cooldown = 0

        self.keys_pressed = set()

    def setup(self):
        settings = SettingsService()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.hit_flash = 0
        self.powerup_message = ''
        self.powerup_timer = 0

        self.player = Player()
        self.bullet_list = []
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_factory = EnemyFactory()
        self.enemy_factory.spawn_interval = settings.get('enemy_spawn_interval', ENEMY_SPAWN_INTERVAL)
        self.enemy_factory.start_next_wave()
        self.powerup_list = []
        self.powerup_spawn_timer = 0
        self.powerup_spawn_interval = 5
        self.bullet_cooldown = 0
        self.explosion_list = []
        self.sound_service = SoundService()

    def load_state(self, data):
        settings = SettingsService()
        self.score = data.get('score', 0)
        self.level = data.get('level', 1)
        self.game_over = False
        self.hit_flash = 0
        self.powerup_message = ''
        self.powerup_timer = 0

        self.player = Player()
        self.player.center_x = data.get('player_x', SCREEN_WIDTH // 2)
        self.player.center_y = data.get('player_y', SCREEN_HEIGHT - 100)
        self.player.health = data.get('health', PLAYER_MAX_HEALTH)
        self.player.shield = data.get('shield', 0)
        self.player.bullet_level = data.get('bullet_level', 1)

        self.bullet_list = []
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_factory = EnemyFactory()
        self.enemy_factory.spawn_interval = settings.get('enemy_spawn_interval', ENEMY_SPAWN_INTERVAL)
        self.enemy_factory.start_next_wave()
        self.powerup_list = []
        self.powerup_spawn_timer = 0
        self.powerup_spawn_interval = 5
        self.bullet_cooldown = 0
        self.explosion_list = []
        self.sound_service = SoundService()

    def save_state(self):
        return {
            'score': self.score,
            'level': self.level,
            'player_x': self.player.center_x,
            'player_y': self.player.center_y,
            'health': self.player.health,
            'shield': self.player.shield,
            'bullet_level': self.player.bullet_level
        }

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.handle_input()
        self.update_bullets()
        self.update_enemy_bullets()
        self.update_enemies()
        self.update_powerups()
        self.update_explosions()
        self.spawn_enemies(delta_time)
        self.spawn_powerups(delta_time)
        self.enemy_shoot()
        self.check_collisions()
        self.check_level_up()

        if self.hit_flash > 0:
            self.hit_flash -= delta_time
        if self.powerup_timer > 0:
            self.powerup_timer -= delta_time
            if self.powerup_timer <= 0:
                self.powerup_message = ''

        if SaveService.has_save():
            SaveService.save(self.save_state())

    def handle_input(self):
        dx, dy = 0, 0
        if 'left' in self.keys_pressed:
            dx -= 1
        if 'right' in self.keys_pressed:
            dx += 1
        if 'up' in self.keys_pressed:
            dy += 1
        if 'down' in self.keys_pressed:
            dy -= 1

        if dx != 0 or dy != 0:
            self.player.move(dx, dy)

        self.bullet_cooldown -= 1/60
        if 'fire' in self.keys_pressed and self.bullet_cooldown <= 0:
            self.shoot()

    def shoot(self):
        self.bullet_cooldown = BULLET_COOLDOWN / self.player.bullet_level
        bullet = Bullet(self.player.center_x, self.player.center_y + 20)
        self.bullet_list.append(bullet)
        self.sound_service.play('shoot')

    def update_bullets(self):
        for bullet in self.bullet_list:
            bullet.update()
        self.bullet_list = [b for b in self.bullet_list if b.active]

    def update_enemy_bullets(self):
        self.enemy_bullet_list.update()

    def update_enemies(self):
        self.enemy_list.update()

    def enemy_shoot(self):
        for enemy in self.enemy_list:
            if enemy.can_shoot():
                self.enemy_bullet_list.append(enemy.shoot())

    def update_powerups(self):
        for powerup in self.powerup_list:
            powerup.update()
        self.powerup_list = [p for p in self.powerup_list if p.active]

    def update_explosions(self):
        for explosion in self.explosion_list:
            explosion.update(1/60)
        self.explosion_list = [e for e in self.explosion_list if e.active]

    def spawn_enemies(self, delta_time):
        enemy = self.enemy_factory.update(delta_time)
        if enemy:
            self.enemy_list.append(enemy)

    def spawn_powerups(self, delta_time):
        self.powerup_spawn_timer += delta_time
        if self.powerup_spawn_timer >= self.powerup_spawn_interval:
            self.powerup_spawn_timer = 0
            powerup = PowerUpFactory.maybe_create(
                random.randint(30, SCREEN_WIDTH - 30),
                SCREEN_HEIGHT + 20
            )
            if powerup:
                self.powerup_list.append(powerup)

    def check_collisions(self):
        player_x = self.player.center_x
        player_y = self.player.center_y
        player_radius = 18

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in self.bullet_list:
            for enemy in self.enemy_list:
                dx = enemy.center_x - bullet.center_x
                dy = enemy.center_y - bullet.center_y
                dist = (dx * dx + dy * dy) ** 0.5
                hit_range = 25 if enemy.ai_type == Enemy.AI_BOSS else 20
                if dist < hit_range:
                    bullets_to_remove.append(bullet)
                    if enemy.take_damage():
                        enemies_to_remove.append(enemy)
                        if enemy.ai_type == Enemy.AI_BOSS:
                            self.score += BOSS_SCORE
                        else:
                            self.score += SCORE_PER_ENEMY
                    break

        for bullet in bullets_to_remove:
            bullet.active = False

        for enemy in enemies_to_remove:
            enemy.kill()
            is_boss = enemy.ai_type == Enemy.AI_BOSS
            self.explosion_list.append(Explosion(enemy.center_x, enemy.center_y, is_boss))
            self.sound_service.play('explosion')
            if is_boss:
                self.sound_service.play('game_over')
            if not is_boss:
                powerup = PowerUpFactory.maybe_create(enemy.center_x, enemy.center_y)
                if powerup:
                    self.powerup_list.append(powerup)

        for enemy in self.enemy_list:
            dx = enemy.center_x - player_x
            dy = enemy.center_y - player_y
            dist = (dx * dx + dy * dy) ** 0.5
            hit_range = player_radius + 25 if enemy.ai_type == Enemy.AI_BOSS else player_radius + 17
            if dist < hit_range:
                enemy.kill()
                self.hit_flash = 0.2
                self.sound_service.play('hit')
                if self.player.take_damage():
                    self.trigger_game_over()

        for powerup in self.powerup_list:
            dx = powerup.center_x - player_x
            dy = powerup.center_y - player_y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < player_radius + 15:
                self.apply_powerup(powerup)
                powerup.active = False

        for bullet in self.enemy_bullet_list:
            dx = bullet.center_x - player_x
            dy = bullet.center_y - player_y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < player_radius + 8:
                bullet.kill()
                self.hit_flash = 0.2
                self.sound_service.play('hit')
                if self.player.take_damage():
                    self.trigger_game_over()

    def apply_powerup(self, powerup):
        if powerup.power_type == PowerUp.TYPE_BULLET:
            self.player.bullet_level = min(3, self.player.bullet_level + 1)
            self.powerup_message = '火力强化！'
        elif powerup.power_type == PowerUp.TYPE_SHIELD:
            self.player.shield = min(3, self.player.shield + 1)
            self.powerup_message = '护盾激活！'
        elif powerup.power_type == PowerUp.TYPE_BOMB:
            for enemy in self.enemy_list:
                enemy.kill()
                self.score += SCORE_PER_ENEMY
            self.powerup_message = '炸弹！'
        self.powerup_timer = 1.5
        self.sound_service.play('powerup')

    def check_level_up(self):
        new_level = self.score // LEVEL_UP_SCORE + 1
        if new_level > self.level:
            self.level = new_level

    def trigger_game_over(self):
        self.game_over = True
        SaveService.clear()
        self.sound_service.play('game_over')

    def draw_player(self):
        x, y = self.player.center_x, self.player.center_y
        color = arcade.color.RED if self.hit_flash > 0 else arcade.color.CYAN

        arcade.draw_polygon_filled([
            (x, y + 20), (x - 20, y - 15), (x - 8, y - 5),
            (x + 8, y - 5), (x + 20, y - 15)
        ], color)

        arcade.draw_polygon_filled([
            (x - 20, y - 5), (x - 30, y - 10), (x - 25, y + 5)
        ], color)

        arcade.draw_polygon_filled([
            (x + 20, y - 5), (x + 30, y - 10), (x + 25, y + 5)
        ], color)

        arcade.draw_circle_filled(x, y + 5, 4, arcade.color.BLUE)

        if self.player.shield > 0:
            arcade.draw_ellipse_outline(x, y, 35, 40, arcade.color.BLUE, 2)

    def draw_health_bar(self):
        bar_width = 100
        bar_height = 15
        bar_x = 10
        bar_y = SCREEN_HEIGHT - 80

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y - bar_height/2, bar_width, bar_height, arcade.color.GRAY)

        health_ratio = self.player.health / PLAYER_MAX_HEALTH
        if health_ratio > 0.5:
            health_color = arcade.color.GREEN
        elif health_ratio > 0.25:
            health_color = arcade.color.ORANGE
        else:
            health_color = arcade.color.RED

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y - bar_height/2, bar_width * health_ratio, bar_height, health_color)
        arcade.draw_text('生命', bar_x, bar_y - 25, arcade.color.WHITE, 12)

    def draw_powerup_status(self):
        arcade.draw_text(f'火力: {"★" * self.player.bullet_level}', SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.YELLOW, 14)
        arcade.draw_text(f'护盾: {self.player.shield}', SCREEN_WIDTH - 120, SCREEN_HEIGHT - 55, arcade.color.BLUE, 14)

    def draw_boss_health(self):
        for enemy in self.enemy_list:
            if enemy.ai_type == Enemy.AI_BOSS:
                bar_width = 80
                bar_height = 8
                bar_x = enemy.center_x - bar_width // 2
                bar_y = enemy.center_y + 35

                arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.DARK_GRAY)
                health_ratio = enemy.health / BOSS_HEALTH
                arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width * health_ratio, bar_height, arcade.color.RED)
                arcade.draw_text('BOSS', enemy.center_x, bar_y + 12, arcade.color.RED, 10, anchor_x='center')

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        arcade.draw_text(f'分数: {self.score}', 10, SCREEN_HEIGHT - 30, arcade.color.GOLD, 18)
        arcade.draw_text(f'波次: {self.enemy_factory.wave}', 10, SCREEN_HEIGHT - 55, arcade.color.WHITE, 16)

        self.draw_health_bar()
        self.draw_powerup_status()
        self.draw_boss_health()

        for bullet in self.bullet_list:
            bullet.draw()

        self.enemy_bullet_list.draw()
        self.enemy_list.draw()

        for powerup in self.powerup_list:
            powerup.draw()

        for explosion in self.explosion_list:
            explosion.draw()

        self.draw_player()

        if self.powerup_message:
            arcade.draw_text(self.powerup_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                           arcade.color.GREEN, 24, anchor_x='center')

        if self.game_over:
            arcade.draw_text('游戏结束', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, arcade.color.RED, 32, anchor_x='center')
            arcade.draw_text('按 R 重新开始  ESC 返回菜单', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, arcade.color.WHITE, 18, anchor_x='center')

        arcade.draw_text('移动: ←→↑↓ 或 WASD   射击: Space/Z   暂停: ESC', SCREEN_WIDTH // 2, 30, arcade.color.GRAY, 12, anchor_x='center')

    def on_key_press(self, key, modifiers):
        key_map = {
            arcade.key.LEFT: 'left', arcade.key.RIGHT: 'right',
            arcade.key.UP: 'up', arcade.key.DOWN: 'down',
            arcade.key.SPACE: 'fire', arcade.key.Z: 'fire',
        }
        name = key_map.get(key)
        if name:
            self.keys_pressed.add(name)

        if key == arcade.key.R and self.game_over:
            self.setup()
        elif key == arcade.key.ESCAPE:
            from src.scenes.menu_scene import MenuScene
            self.window.show_view(MenuScene())

    def on_key_release(self, key, modifiers):
        key_map = {
            arcade.key.LEFT: 'left', arcade.key.RIGHT: 'right',
            arcade.key.UP: 'up', arcade.key.DOWN: 'down',
            arcade.key.SPACE: 'fire', arcade.key.Z: 'fire',
        }
        name = key_map.get(key)
        if name and name in self.keys_pressed:
            self.keys_pressed.discard(name)
