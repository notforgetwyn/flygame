import arcade
from src.constants import *
from src.models.player import Player
from src.models.bullet import Bullet
from src.models.enemy import Enemy
from src.models.enemy_factory import EnemyFactory


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.level = 1
        self.game_over = False

        self.player_sprite = None
        self.bullet_list = None
        self.enemy_list = None
        self.enemy_factory = None
        self.bullet_cooldown = 0

        self.keys_pressed = set()

    def setup(self):
        self.score = 0
        self.level = 1
        self.game_over = False

        self.player_sprite = Player()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_factory = EnemyFactory()
        self.bullet_cooldown = 0

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.handle_input()
        self.update_bullets()
        self.update_enemies()
        self.spawn_enemies(delta_time)
        self.check_collisions()
        self.check_level_up()

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
            self.player_sprite.move(dx, dy)

        self.bullet_cooldown -= 1/60
        if 'fire' in self.keys_pressed and self.bullet_cooldown <= 0:
            self.shoot()

    def shoot(self):
        self.bullet_cooldown = BULLET_COOLDOWN
        bullet = Bullet(self.player_sprite.center_x, self.player_sprite.center_y + 20)
        self.bullet_list.append(bullet)

    def update_bullets(self):
        self.bullet_list.update()

    def update_enemies(self):
        self.enemy_list.update()

    def spawn_enemies(self, delta_time):
        enemy = self.enemy_factory.update(delta_time)
        if enemy:
            self.enemy_list.append(enemy)

    def check_collisions(self):
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                enemy.kill()
                bullet.kill()
                self.score += SCORE_PER_ENEMY

        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy, self.player_sprite):
                enemy.kill()
                if self.player_sprite.take_damage():
                    self.trigger_game_over()

    def check_level_up(self):
        new_level = self.score // LEVEL_UP_SCORE + 1
        if new_level > self.level:
            self.level = new_level
            self.enemy_factory.spawn_interval = max(0.3, ENEMY_SPAWN_INTERVAL - (self.level - 1) * 0.15)

    def trigger_game_over(self):
        self.game_over = True

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        arcade.draw_text(f'分数: {self.score}', 10, SCREEN_HEIGHT - 30,
                         arcade.color.GOLD, 18)
        arcade.draw_text(f'关卡: {self.level}', 10, SCREEN_HEIGHT - 55,
                         arcade.color.WHITE, 16)
        arcade.draw_text(f'生命: {self.player_sprite.health}', 10, SCREEN_HEIGHT - 80,
                         arcade.color.GREEN, 16)

        self.bullet_list.draw()
        self.enemy_list.draw()
        arcade.draw_sprite(self.player_sprite)

        if self.game_over:
            arcade.draw_text('游戏结束', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
                             arcade.color.RED, 32, anchor_x='center')
            arcade.draw_text('按 R 重新开始  ESC 返回菜单', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                             arcade.color.WHITE, 18, anchor_x='center')

    def on_key_press(self, key, modifiers):
        key_map = {
            arcade.key.LEFT: 'left',
            arcade.key.RIGHT: 'right',
            arcade.key.UP: 'up',
            arcade.key.DOWN: 'down',
            arcade.key.SPACE: 'fire',
            arcade.key.Z: 'fire',
        }
        name = key_map.get(key)
        if name:
            self.keys_pressed.add(name)

        if key == arcade.key.R and self.game_over:
            self.setup()
        elif key == arcade.key.ESCAPE:
            from src.app import App
            App.show_menu()

    def on_key_release(self, key, modifiers):
        key_map = {
            arcade.key.LEFT: 'left',
            arcade.key.RIGHT: 'right',
            arcade.key.UP: 'up',
            arcade.key.DOWN: 'down',
            arcade.key.SPACE: 'fire',
            arcade.key.Z: 'fire',
        }
        name = key_map.get(key)
        if name and name in self.keys_pressed:
            self.keys_pressed.discard(name)