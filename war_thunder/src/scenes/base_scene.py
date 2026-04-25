from abc import ABC


class BaseScene(ABC):
    def __init__(self):
        pass

    def handle_event(self, key):
        pass

    def update(self, delta_time):
        pass

    def render(self):
        pass
