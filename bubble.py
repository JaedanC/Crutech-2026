from typing import Tuple
from shapes import Circle, add_tuple
import random
import pygui_cython as pygui


class Bubble(Circle):
    def __init__(self, position, radius, gravity: pygui.Float):
        super().__init__(position, radius, (1, 0.4, 0.4, 1), False)
        self.velocity = [
            3 * random.choice([1, -1]),
            random.random() * 2 - 1
        ]
        self.gravity = gravity

    
    def tick(self, sandbox_size: Tuple[float, float]):
        # Left right bounds
        new_position_x = self.position.x + self.velocity[0]
        if new_position_x < 0 or new_position_x > sandbox_size[0]:
            self.velocity[0] = -self.velocity[0]


        # Up down bounds
        new_position_y = self.position.y + self.velocity[1]
        if new_position_y > sandbox_size[1]:
            self.velocity[1] = -self.velocity[1]
        else:
            # Apply gravity
            self.velocity[1] += self.gravity.value
        
        self.position.x += self.velocity[0]
        self.position.y += self.velocity[1]
        