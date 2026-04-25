import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.text import TextBlock
from src.ui.menu_list import MenuList
from src.core.settings_service import SettingsService


class SettingsScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.settings = SettingsService()
        self.menu = MenuList(['难度调整', '返回主菜单'], SCREEN_HEIGHT - 220, item_height=50)
        self.difficulty = self.settings.get('enemy_speed', 3)
        self.spawn_interval = self.settings.get('enemy_spawn_interval', 1.5)
        self.message = ''

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        TextBlock('设置', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, 32, arcade.color.GOLD, 'center').draw()

        TextBlock(f'敌机速度: {self.difficulty}', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180, 20, arcade.color.WHITE, 'center').draw()
        TextBlock(f'生成间隔: {self.spawn_interval:.1f}秒', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 210, 20, arcade.color.WHITE, 'center').draw()

        self.menu.draw()

        if self.message:
            TextBlock(self.message, SCREEN_WIDTH // 2, 150, 16, arcade.color.GREEN, 'center').draw()

        TextBlock('A/D 调整数值   Enter 保存   ESC 返回', SCREEN_WIDTH // 2, 80, 14, arcade.color.GRAY, 'center').draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from src.scenes.menu_scene import MenuScene
            self.window.show_view(MenuScene())
            return

        if self.menu.handle_key(key):
            return

        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            selected = self.menu.get_selected()
            if selected == '难度调整':
                self.settings.set('enemy_speed', self.difficulty)
                self.settings.set('enemy_spawn_interval', self.spawn_interval)
                self.settings.save()
                self.message = '设置已保存'
            elif selected == '返回主菜单':
                from src.scenes.menu_scene import MenuScene
                self.window.show_view(MenuScene())
        elif key == arcade.key.A or key == arcade.key.D:
            selected = self.menu.get_selected()
            if selected == '难度调整':
                if key == arcade.key.A:
                    self.difficulty = max(1, self.difficulty - 1)
                    self.spawn_interval = min(3.0, self.spawn_interval + 0.2)
                else:
                    self.difficulty = min(10, self.difficulty + 1)
                    self.spawn_interval = max(0.3, self.spawn_interval - 0.2)
                self.message = '按 Enter 保存设置'
