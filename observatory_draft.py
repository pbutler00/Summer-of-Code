import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Interactive Nighttime Observation Game'



class TextButton:
    """
    ____________________________________________________________
    |    Sourced from Python Arcade Library Examples:          |
    |    https://arcade.academy/examples/gui_text_button.html  |
    ------------------------------------------------------------
    """


    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.WHITE_SMOKE,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()

def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()

class DiscoveredButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Objects Discovered", 10, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class InstructionsButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Instructions", 12, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

"""
ORIGINAL CODE
"""

class IntroView(arcade.View):
    def on_show(self):
        self.intro_background = arcade.load_texture("images/start_menu_back.jpeg")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.intro_background)

        arcade.draw_text("Interactive Astronomy Observation", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Summer of Code 2020", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("(Click to begin)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)

class MainGame(arcade.View):

    def __init__(self):
        super().__init__()

        #setting background for back image
        self.background = None

        #telescopes
        self.binoculars = None
        self.small = None
        self.large = None
        self.observatory = None
        self.telescope_list = arcade.SpriteList()

        self.button_list = None
        self.click_sound = None
        self.end = False

    def setup(self):
        # sounds

        self.back_music = arcade.load_sound("sounds/back_tester.mp3")

        #background image
        self.background = arcade.load_texture("images/background.jpg")

        #hamilton logo?


        #buttons
        # Create our on-screen GUI buttons
        self.button_list = []

        discovered_button = DiscoveredButton(200, 50,self.display_discovered())
        self.button_list.append(discovered_button)

        instructions_button = InstructionsButton(400, 50,self.display_instructions())
        self.button_list.append(instructions_button)

        #telescope sprites
        self.binoculars = arcade.Sprite("images/binoculars.png", scale = 0.075,
                                        center_x= 100, center_y= 400)
        self.telescope_list.append(self.binoculars)

        self.small = arcade.Sprite("images/small.png",scale = 0.2,
                                   center_x=300, center_y=400)
        self.telescope_list.append(self.small)

        self.large = arcade.Sprite("images/large.png", scale = 0.8,
                                        center_x=500, center_y=400)
        self.telescope_list.append(self.large)

        self.observatory = arcade.Sprite("images/observatory.png", scale=0.15,
                                   center_x=700, center_y=400)
        self.telescope_list.append(self.observatory)


    def on_draw(self):

        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # start background music (looped?)
        """DO NOT PLAY THIS SOUND! IT WILL HURT YOUR EARS!"""
        #arcade.play_sound(self.back_music)

        # Drawing sprites
        self.binoculars.draw()
        self.small.draw()
        self.large.draw()
        self.observatory.draw()

        #buttons
        for button in self.button_list:
            button.draw()

    def on_update(self, delta_time):
        """
        Game Logic goes here!
        """
        pass

    def on_key_press(self, key, key_modifiers):

        pass

    def on_key_release(self, key, key_modifiers):

        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):

        pass

    def on_mouse_press(self, x, y, button, key_modifiers):

        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):

        check_mouse_release_for_buttons(x, y, self.button_list)

    def display_instructions(self):
        pass

    def display_discovered(self):
        pass

class BinocularView(arcade.View):
    def on_show(self):
        self.binocular_back = arcade.load_texture("images/binocular_back.png")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.binocular_back)

class SmallView(arcade.View):
    def on_show(self):
        self.small_back = arcade.load_texture("images/small_back.png")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.small_back)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)

class LargeView(arcade.View):
    def on_show(self):
        self.large_back = arcade.load_texture("images/large_back.png")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.large_back)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)

class ObservatoryView(arcade.View):

    def on_show(self):
        self.observatory_back = arcade.load_texture("images/observatory_back.png")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.observatory_back)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)



def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
