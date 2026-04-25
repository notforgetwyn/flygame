import arcade
from src.constants import *
from src.models.enemy import Enemy
from src.models.enemy_factory import EnemyFactory
from src.core.save_service import SaveService
from src.core.settings_service import SettingsService


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


class GameScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.hit_flash = 0

        self.player = None
        self.bullet_list = []
        self.enemy_list = None
        self.enemy_factory = None
        self.bullet_cooldown = 0

        self.keys_pressed = set()

    def setup(self):
        settings = SettingsService()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.hit_flash = 0

        self.player = Player()
        self.bullet_list = []
        self.enemy_list = arcade.SpriteList()
        self.enemy_factory = EnemyFactory()
        self.enemy_factory.spawn_interval = settings.get('enemy_spawn_interval', ENEMY_SPAWN_INTERVAL)
        self.bullet_cooldown = 0

    def load_state(self, data):
        settings = SettingsService()
        self.score = data.get('score', 0)
        self.level = data.get('level', 1)
        self.game_over = False
        self.hit_flash = 0

        self.player = Player()
        self.player.center_x = data.get('player_x', SCREEN_WIDTH // 2)
        self.player.center_y = data.get('player_y', SCREEN_HEIGHT - 100)
        self.player.health = data.get('health', PLAYER_MAX_HEALTH)

        self.bullet_list = []
        self.enemy_list = arcade.SpriteList()
        self.enemy_factory = EnemyFactory()
        self.enemy_factory.spawn_interval = settings.get('enemy_spawn_interval', ENEMY_SPAWN_INTERVAL)
        self.bullet_cooldown = 0

    def save_state(self):
        return {
            'score': self.score,
            'level': self.level,
            'player_x': self.player.center_x,
            'player_y': self.player.center_y,
            'health': self.player.health
        }

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.handle_input()
        self.update_bullets()
        self.update_enemies()
        self.spawn_enemies(delta_time)
        self.check_collisions()
        self.check_level_up()

        if self.hit_flash > 0:
            self.hit_flash -= delta_time

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
        self.bullet_cooldown = BULLET_COOLDOWN
        bullet = Bullet(self.player.center_x, self.player.center_y + 20)
        self.bullet_list.append(bullet)

    def update_bullets(self):
        for bullet in self.bullet_list:
            bullet.update()
        self.bullet_list = [b for b in self.bullet_list if b.active]

    def update_enemies(self):
        self.enemy_list.update()

    def spawn_enemies(self, delta_time):
        enemy = self.enemy_factory.update(delta_time)
        if enemy:
            self.enemy_list.append(enemy)

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
                if dist < 20:
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    self.score += SCORE_PER_ENEMY
                    break

        for bullet in bullets_to_remove:
            bullet.active = False

        for enemy in enemies_to_remove:
            enemy.kill()

        for enemy in self.enemy_list:
            dx = enemy.center_x - player_x
            dy = enemy.center_y - player_y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < player_radius + 17:
                enemy.kill()
                self.hit_flash = 0.2
                if self.player.take_damage():
                    self.trigger_game_over()

    def check_level_up(self):
        new_level = self.score // LEVEL_UP_SCORE + 1
        if new_level > self.level:
            self.level = new_level

    def trigger_game_over(self):
        self.game_over = True
        SaveService.clear()

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

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        arcade.draw_text(f'分数: {self.score}', 10, SCREEN_HEIGHT - 30, arcade.color.GOLD, 18)
        arcade.draw_text(f'关卡: {self.level}', 10, SCREEN_HEIGHT - 55, arcade.color.WHITE, 16)

        self.draw_health_bar()

        for bullet in self.bullet_list:
            bullet.draw()

        self.enemy_list.draw()
        self.draw_player()

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
