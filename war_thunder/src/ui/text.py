import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TextBlock:
    def __init__(self, text, x, y, font_size=18, color=None, anchor_x='left', anchor_y='bottom'):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color or arcade.color.WHITE
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def draw(self):
        arcade.draw_text(self.text, self.x, self.y,
                        self.color, self.font_size,
                        anchor_x=self.anchor_x, anchor_y=self.anchor_y)

    @staticmethod
    def center_x(y, font_size=18):
        return SCREEN_WIDTH // 2, y

    @staticmethod
    def top(y, font_size=18):
        return y, SCREEN_HEIGHT - y
