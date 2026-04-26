import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, arcade
from src.ui.text import TextBlock
from src.ui.menu_list import MenuList
from src.core.save_service import SaveService
from src.core.sound_service import SoundService


class MenuScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = MenuList(['开始游戏', '继续游戏', '设置', '退出游戏'], SCREEN_HEIGHT - 200)
        self.sound_service = SoundService()
        if not self.sound_service._music_player:
            self.sound_service.play_music(looping=True)

    def on_show_view(self):
        """当视图显示时"""
        try:
            if self.sound_service and self.sound_service._music_player:
                self.sound_service.resume_music()
        except:
            pass

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        # 装饰线条
        arcade.draw_line(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 140, SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 140, arcade.color.GOLD, 2)
        arcade.draw_line(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 142, SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT - 142, arcade.color.GOLD, 1)

        TextBlock('战争飞机雷霆', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 36, arcade.color.GOLD, 'center').draw()

        # 副标题
        TextBlock('War Thunder Lightning', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 145, 14, arcade.color.GRAY, 'center').draw()

        self.menu.draw()

        # 装饰线条
        arcade.draw_line(SCREEN_WIDTH // 2 - 100, 60, SCREEN_WIDTH // 2 + 100, 60, arcade.color.GRAY, 1)
        arcade.draw_line(SCREEN_WIDTH // 2 - 80, 62, SCREEN_WIDTH // 2 + 80, 62, arcade.color.GRAY, 1)

        TextBlock('方向键/WASD 选择  Enter 执行', SCREEN_WIDTH // 2, 40, 14, arcade.color.GRAY, 'center').draw()

    def on_key_press(self, key, modifiers):
        if self.menu.handle_key(key):
            return
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.select_item()

    def select_item(self):
        selected = self.menu.get_selected()
        if selected == '开始游戏':
            SaveService.clear()
            from src.scenes.game_scene import GameScene
            game = GameScene()
            game.setup()
            self.window.show_view(game)
        elif selected == '继续游戏':
            from src.scenes.continue_scene import ContinueScene
            self.window.show_view(ContinueScene())
        elif selected == '设置':
            from src.scenes.settings_scene import SettingsScene
            self.window.show_view(SettingsScene())
        elif selected == '退出游戏':
            arcade.exit()
