import arcade
from src.constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.menu_scene import MenuScene


class App:
    window = None

    @staticmethod
    def start():
        App.window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        menu = MenuScene()
        App.window.show_view(menu)
        arcade.run()
