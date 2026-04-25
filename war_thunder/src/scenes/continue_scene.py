import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.text import TextBlock
from src.core.save_service import SaveService


class ContinueScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.has_save = SaveService.has_save()
        self.save_data = SaveService.load() if self.has_save else None

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        TextBlock('继续游戏', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 32, arcade.color.GOLD, 'center').draw()

        if self.has_save and self.save_data:
            TextBlock('有存档', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180, 20, arcade.color.GREEN, 'center').draw()
            TextBlock(f"分数: {self.save_data.get('score', 0)}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220, 18, arcade.color.WHITE, 'center').draw()
            TextBlock(f"关卡: {self.save_data.get('level', 1)}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250, 18, arcade.color.WHITE, 'center').draw()
            TextBlock('Enter 继续游戏', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 320, 18, arcade.color.WHITE, 'center').draw()
        else:
            TextBlock('暂无存档', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180, 20, arcade.color.RED, 'center').draw()
            TextBlock('请先开始新游戏', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220, 16, arcade.color.GRAY, 'center').draw()

        TextBlock('ESC 返回主菜单', SCREEN_WIDTH // 2, 100, 14, arcade.color.GRAY, 'center').draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from src.scenes.menu_scene import MenuScene
            self.window.show_view(MenuScene())
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.has_save:
                from src.scenes.game_scene import GameScene
                game = GameScene()
                game.load_state(self.save_data)
                self.window.show_view(game)
            else:
                from src.scenes.menu_scene import MenuScene
                self.window.show_view(MenuScene())
