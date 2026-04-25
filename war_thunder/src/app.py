import arcade
from .menu_window import MenuWindow
from .game_window import GameWindow


class App:
    window = None

    @staticmethod
    def show_menu():
        if App.window:
            App.window.close()
        App.window = MenuWindow()
        App.window.run()

    @staticmethod
    def show_game():
        if App.window:
            App.window.close()
        App.window = GameWindow()
        App.window.setup()
        App.window.run()
