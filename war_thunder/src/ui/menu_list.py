import arcade
from src.constants import SCREEN_WIDTH


class MenuList:
    def __init__(self, items, start_y, item_height=50, font_size=22):
        self.items = items
        self.selected_index = 0
        self.start_y = start_y
        self.item_height = item_height
        self.font_size = font_size
        self.selected_color = arcade.color.ORANGE
        self.normal_color = arcade.color.WHITE

    def move_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.items)

    def get_selected(self):
        return self.items[self.selected_index]

    def draw(self):
        for i, item in enumerate(self.items):
            y = self.start_y - i * self.item_height
            color = self.selected_color if i == self.selected_index else self.normal_color
            prefix = '> ' if i == self.selected_index else '  '
            arcade.draw_text(f'{prefix}{item}', SCREEN_WIDTH // 2, y,
                           color, self.font_size, anchor_x='center')

    def handle_key(self, key):
        if key == arcade.key.UP or key == arcade.key.W:
            self.move_up()
            return True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.move_down()
            return True
        return False
