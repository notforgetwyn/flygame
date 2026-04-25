import arcade
from src.constants import *


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_items = ['开始游戏', '继续游戏', '设置', '退出游戏']
        self.selected_index = 0

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        arcade.draw_text('战争飞机雷霆', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120,
                         arcade.color.GOLD, 36, anchor_x='center', font_name='Times New Roman')

        for i, item in enumerate(self.menu_items):
            color = arcade.color.ORANGE if i == self.selected_index else arcade.color.WHITE
            arcade.draw_text(item, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220 - i * 50,
                           color, 22, anchor_x='center')

        arcade.draw_text('方向键/WASD 选择  Enter 执行', SCREEN_WIDTH // 2, 100,
                        arcade.color.GRAY, 14, anchor_x='center')

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.select_item()

    def select_item(self):
        if self.selected_index == 0:
            from src.app import App
            App.start_game()
        elif self.selected_index == 3:
            arcade.exit()