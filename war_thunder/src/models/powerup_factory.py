import random
from src.models.powerup import PowerUp


class PowerUpFactory:
    DROP_CHANCE = 0.15

    def __init__(self):
        pass

    @staticmethod
    def maybe_create(x, y):
        if random.random() < PowerUpFactory.DROP_CHANCE:
            power_type = random.choice([
                PowerUp.TYPE_BULLET,
                PowerUp.TYPE_SHIELD,
                PowerUp.TYPE_BOMB
            ])
            return PowerUp(x, y, power_type)
        return None
