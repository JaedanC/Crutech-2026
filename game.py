import math
import pygui_cython as pygui


class Game:
    def __init__(self):
        self.first_frame = True

    def on_start(self):
        """
        On game start do this. Save any variables you want to initilise with
        self.variable_name = [value_to_start_with]
        """
        self.window_width, self.window_height = pygui.get_content_region_avail()
        self.player_position = pygui.Vec2(self.window_width / 2, self.window_height / 2)
        self.player_health = pygui.Int(100)

    def draw(self):
        """
        Every game tick/frame this is called. This is where your game logic goes
        """
        main_viewport = pygui.get_main_viewport()
        id_ = pygui.get_id("Main view")
        ds = pygui.dock_space_over_viewport(dockspace_id=id_, viewport=main_viewport)
        pygui.set_next_window_dock_id(ds, pygui.COND_ALWAYS)

        # To create a new panel, we must use a pygui.begin() and a pygui.end().
        # The pygui.end() must ALWAYS be called. It most not be "nested" inside
        # the pygui.begin().
        if pygui.begin("Main window"):
            if self.first_frame:
                self.on_start()

            cx, cy = pygui.get_cursor_screen_pos()
            dl = pygui.get_window_draw_list()


            frames_since_game_start = pygui.get_frame_count()
            self.player_health.value = 100 + 50 * math.sin(math.pi * (frames_since_game_start / 200))

            dl.add_circle_filled(
                (
                    cx + self.player_position.x, 
                    cy + self.player_position.y
                ),
                100,
                pygui.Vec4(0, 1, 0, 1).to_u32()
            )
        
        pygui.end()

        if pygui.begin("Tools"):
            pygui.text(f"Player Health: {self.player_health.value}")
            pygui.text(f"Player Pos: {self.player_position.tuple()}")
        pygui.end()
