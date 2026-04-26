import arcade
import math
import random


class Explosion:
    def __init__(self, x, y, is_boss=False):
        self.center_x = x
        self.center_y = y
        self.active = True
        self.is_boss = is_boss

        num_particles = 15 if not is_boss else 25
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6) if not is_boss else random.uniform(3, 8)
            size = random.uniform(2, 5) if not is_boss else random.uniform(4, 8)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'alpha': 255,
                'color': random.choice([
                    arcade.color.ORANGE,
                    arcade.color.RED,
                    arcade.color.YELLOW,
                    arcade.color.DARK_ORANGE,
                ])
            })

    def update(self, delta_time):
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= 0.1
            p['alpha'] -= 15
            p['size'] *= 0.95

        self.particles = [p for p in self.particles if p['alpha'] > 0]
        if not self.particles:
            self.active = False

    def draw(self):
        for p in self.particles:
            arcade.draw_circle_filled(
                p['x'], p['y'], p['size'],
                (*p['color'][:3], max(0, p['alpha']))
            )
