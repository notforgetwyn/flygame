import arcade
from src.menu_window import MenuView
from src.game_window import GameView
from src.constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT


class App:
    window = None

    @staticmethod
    def start():
        App.window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        menu = MenuView()
        App.window.show_view(menu)
        arcade.run()

    @staticmethod
    def start_game():
        if App.window:
            game = GameView()
            game.setup()
            App.window.show_view(game)

    @staticmethod
    def show_menu():
        if App.window:
            menu = MenuView()
            App.window.show_view(menu)