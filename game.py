from typing import List
import pygui_cython as pygui
from shapes import *
from ball import Ball
import random


class Game:
    def __init__(self):
        self.first_frame = True

    def on_start(self):
        """
        On game start do this. Save any variables you want to initilise with
        self.variable_name = [value_to_start_with]
        """
        self.sandbox_size = pygui.Vec2(500, 500)
        self.player = Rect(
            pygui.Vec2(250, 460),
            pygui.Vec4(0, 1, 0, 1),
            pygui.Vec2(30, 40),
            pygui.Bool(True),
        )
        # self.player = Circle(
        #     pygui.Vec2(self.sandbox_size.x / 2, self.sandbox_size.y / 2),
        #     pygui.Vec4(0, 1, 0, 1),
        #     pygui.Float(15),
        #     pygui.Bool(True),
        #     pygui.Float(3),
        # )
        # self.ball = Ball(
        #     pygui.Vec2(0, 0),
        #     pygui.Float(18),
        #     pygui.Vec2(1, 0),
        #     pygui.Vec4(0, 0, 1, 1),
        #     pygui.Float(0)
        # )
        self.balls = []
        self.player_speed = pygui.Int(10)
        self.wall = Rect(
            pygui.Vec2(250, 491),
            pygui.Vec4(1, 0, 1, 1),
            pygui.Vec2(500, 20),
            pygui.Bool(True),
        )
        self.spike = None
        self.game_objects: List[Shape] = [
            self.player,
            self.wall,
        ]

        self.game_paused = pygui.Bool(False)
        self.john2 = pygui.Bool(False)

    def _push_game_window(self):
        """All this function does is give us the drawing 'Sandbox' we see in the
        Game window. The origin is the TOP LEFT coordinate of the Game Sandbox. This
        value is called the origin.

        When drawing, it's important that we pass the origin to the draw function.
        Therefore, treat game entities as relative to this. i.e. And entity with
        Position (0, 0) should be drawn at the TOP LEFT of the sandbox (origin + pos).
        The draw funtion will handle this.
        """
        self.window_size = pygui.get_content_region_avail()
        origin = pygui.get_cursor_screen_pos()
        draw_list = pygui.get_window_draw_list()

        # First clip rect is the whole window so the sandbox doesn't go outside the window.
        draw_list.push_clip_rect(
            origin,
            add_tuple(origin, self.window_size),
        )
        centre_of_window = (self.window_size[0] / 2, self.window_size[1] / 2)
        top_left_sandbox = (
            centre_of_window[0] - self.sandbox_size.x / 2,
            centre_of_window[1] - self.sandbox_size.y / 2
        )
        bottom_right_sandbox = (
            centre_of_window[0] + self.sandbox_size.x / 2,
            centre_of_window[1] + self.sandbox_size.y / 2,
        )
        # Second clip rect is for the Sandbox so that the game doesn't draw outside the sandbox.
        draw_list.push_clip_rect(
            add_tuple(origin, top_left_sandbox),
            add_tuple(origin, bottom_right_sandbox),
            intersect_with_current_clip_rect=True
        )
        draw_list.add_rect(
            add_tuple(origin, top_left_sandbox),
            add_tuple(origin, bottom_right_sandbox),
            pygui.Vec4(0.7, 0.7, 0.7, 1).to_u32(),
            thickness=5
        )
        pygui.set_cursor_screen_pos(add_tuple(origin, top_left_sandbox))
        origin = pygui.get_cursor_screen_pos()
        pygui.dummy((0, 0))

        return origin, draw_list

    def _pop_game_window(self, draw_list: pygui.ImDrawList):
        draw_list.pop_clip_rect()
        draw_list.pop_clip_rect()

    def draw(self):
        """
        Every game tick/frame this is called. This is where your game logic goes
        """
        ds = pygui.dock_space_over_viewport(
            pygui.get_id("Main view"),
            pygui.get_main_viewport()
        )
        # This forces the Game window to be "docked" inside the Viewport.
        pygui.set_next_window_dock_id(ds, pygui.COND_ALWAYS)

        # To create a window, we must use a pygui.begin() and a pygui.end().
        # The pygui.end() must ALWAYS be called. It must not be "nested" inside
        # the pygui.begin().
        if pygui.begin("Game window"):
            if self.first_frame:
                self.on_start()
                self.first_frame = False

            origin, draw_list = self._push_game_window()

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Let's make the player rainbow. We'll use the frame count to do this
            frames_since_start = pygui.get_frame_count()
            self.player.set_colour_hsv(frames_since_start % 255, 255, 255)
            
            # Let's move the player, but constrain them to the sandbox. Use WASD
            left_right = int(pygui.is_key_down(pygui.KEY_D)) - int(pygui.is_key_down(pygui.KEY_A))
            up_down    = int(pygui.is_key_down(pygui.KEY_S)) - int(pygui.is_key_down(pygui.KEY_W))
            self.player.position.x += left_right * self.player_speed.value
            self.player.position.y += up_down * self.player_speed.value
            clamp_vec2(self.player.position, (0, 0), self.sandbox_size)

            if self.john2.value:
                self.player.radius.value += 1
            
            # self.ball.tick()
            for b in self.balls:
                b: Ball
                b.set_colour_hsv(frames_since_start + random.randint(0, 255), 255, 255)
                b.tick(self.sandbox_size)
            
            if pygui.is_key_down(pygui.KEY_SPACE) and self.spike is None:
                self.spike = Rect(
                    pygui.Vec2(self.player.position.x, self.player.position.y - self.player.size.y / 2),
                    pygui.Vec4(1, 1, 1, 1),
                    pygui.Vec2(4, 0),
                    pygui.Bool(True),
                )

            if self.spike is not None:
                # Update the spike
                speed = 5
                self.spike.size.y += speed * 2
                self.spike.position.y -= speed

                # Kill the spike when it reaches the top or reaches a ball
                reached_the_top = (self.spike.position.y - self.spike.size.y / 2) < 0
                touched_a_ball = False # We'll implement this later. For now, let's make this False
                if reached_the_top or touched_a_ball:
                    self.spike = None
                
            if self.spike is not None:
                self.spike.draw(origin, draw_list)


            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------


            for obj in self.game_objects + self.balls:
                obj.draw(origin, draw_list)


            self._pop_game_window(draw_list)
        pygui.end()

        if pygui.begin("Tools"):
            if pygui.button("Create ball"):
                # Create a ball...
                for _ in range(100):
                    self.balls.append(Ball(
                        pygui.Vec2(random.randint(0, 500), random.randint(0, 100)),
                        pygui.Float(10),
                        pygui.Vec2(
                            random.random() * 2 - 1,
                            random.random() * 2 - 1
                        ),
                        pygui.Vec4(0, 0, 1, 1),
                        pygui.Float(1.1)
                    ))

            pygui.slider_float2("Game Window Size", self.sandbox_size.as_floatptrs(), 1, 1000)
            if pygui.tree_node("Player", pygui.TREE_NODE_FLAGS_DEFAULT_OPEN):
                pygui.slider_float2("Position", self.player.position.as_floatptrs(), 0, self.sandbox_size[0])
                pygui.color_edit3("Colour",     self.player.colour)
                # pygui.slider_float("Radius",    self.player.radius, 1, 200)
                pygui.slider_float2("Size", self.player.size.as_floatptrs(), 0, 500)
                pygui.checkbox("Filled",        self.player.is_filled)
                if self.player.is_filled:
                    pygui.begin_disabled()
                pygui.slider_float("Player Thickness", self.player.thickness, 1, 10)
                if self.player.is_filled:
                    pygui.end_disabled()
                pygui.slider_int("Speed", self.player_speed, 1, 20)
                pygui.checkbox("Truth nukeify", self.john2)
                pygui.color_picker4("Wall Colour", self.wall.colour)
                pygui.tree_pop()
        pygui.end()
