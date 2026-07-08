from typing import Tuple
from shapes import Circle
import pygui_cython as pygui


class Ball(Circle):
    def __init__(
            self,
            position: pygui.Vec2,
            radius: pygui.Float,
            velocity: pygui.Vec2,
            colour: pygui.Vec4,
            bounciness: pygui.Float
        ):
        super().__init__(position, colour, radius, pygui.Bool(True))
        self.velocity = velocity
        self.bounciness = bounciness
    
    def tick(self, bounds: pygui.Vec2):
        # Gravity
        self.velocity.y += 0.05


        # Update position by our velocity
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        if self.position.y > bounds.y or self.position.y < 0:
            self.velocity.y = -self.velocity.y
        
        if self.position.x > bounds.x or self.position.x < 0:
            self.velocity.x = -self.velocity.x
