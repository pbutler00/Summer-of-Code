import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Interactive Astronomy Observation at Hamilton"


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
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,800,115,
                                     arcade.color.NAVY_BLUE,0)

        arcade.draw_text("Interactive Astronomy Observation (at Hamilton!)",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 ,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_text("Summer of Code 2020", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("[Click to begin]", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

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
        self.bin_tally = 0
        self.small_tally = 0
        self.large_tally = 0
        self.obs_tally = 0
        self.total = 0
        self.end = False

    def setup(self):
        # sounds

        self.back_music = arcade.load_sound("sounds/background_game_music.wav")
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")
        #background image
        self.background = arcade.load_texture("images/background.jpg")

        #buttons
        self.button_list = []

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

        # start background music
        self.back_music.play(volume=0.02)

    def on_draw(self):

        arcade.start_render()

        # draw background image
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # draw telescopes
        self.telescope_list.draw()

        #buttons
        for button in self.button_list:
            button.draw()

        #Telescope Labels

        arcade.draw_text("Press B", 100, 500,
                    arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Press T", 300, 500,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Press R", 500, 500,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Press O", 700, 500,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        #instructions and tools labels
        arcade.draw_text("[Press I for instructions]", 200, 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("[Press Space for Objects List]", 600, 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):

        if key == arcade.key.B:
            self.display_binocular_view()
            self.click_sound.play(volume=0.5)
            if self.bin_tally < 1:
                self.bin_tally += 1
            self.add_tally("B")

        elif key == arcade.key.T:
            self.display_small_view()
            self.click_sound.play(volume=0.5)
            print(self.add_tally("T"))
        elif key == arcade.key.R:
            self.display_large_view()
            self.click_sound.play(volume=0.5)
            print(self.add_tally("R"))
        elif key == arcade.key.O:
            self.display_observatory_view()
            self.click_sound.play(volume=0.5)
            print(self.add_tally("O"))
        elif key == arcade.key.I:
            self.display_instruction_view()
            self.click_sound.play(volume=0.5)
        elif key == arcade.key.SPACE:
            self.display_objects_view()
            self.click_sound.play(volume=0.5)
        elif key == arcade.key.ESCAPE:
            self.display_goodbye()

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)

    def add_tally(self,var):
        if var == "B" and self.bin_tally == 0:
            self.bin_tally += 1
            self.total += 1
        if var == "T" and self.small_tally == 0:
            self.small_tally += 1
            self.total += 1
        if var == "R" and self.large_tally == 0:
            self.large_tally += 1
            self.total += 1
        if var == "O" and self.obs_tally == 0:
            self.obs_tally += 1
            self.total += 1
        return(self.total)

    #methods to change view for each telescope
    def display_binocular_view(self):
        new_view = BinocularView()
        self.window.show_view(new_view)

    def display_small_view(self):
        new_view = SmallView()
        self.window.show_view(new_view)

    def display_large_view(self):
        new_view = LargeView()
        self.window.show_view(new_view)

    def display_observatory_view(self):
        new_view = ObservatoryView()
        self.window.show_view(new_view)

    # changing displays for other menu functions

    def display_instruction_view(self):
        new_view = InstructionsView()
        self.window.show_view(new_view)

    def display_objects_view(self):
        new_view = ObjectsView()
        self.window.show_view(new_view)
    def display_goodbye(self):
        new_view = EndView()
        self.window.show_view(new_view)

#view for each telescope
class BinocularView(arcade.View):
    def on_show(self):
        self.binocular_back = arcade.load_texture("images/binocular_back.png")
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.binocular_back)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)
        self.click_sound.play(volume=0.5)

class SmallView(arcade.View):
    def on_show(self):
        self.small_back = arcade.load_texture("images/small_back.png")
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

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
        self.click_sound.play(volume=0.5)

class LargeView(arcade.View):
    def on_show(self):
        self.large_back = arcade.load_texture("images/large_back.png")
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

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
        self.click_sound.play(volume=0.5)

class ObservatoryView(arcade.View):

    def on_show(self):
        self.observatory_back = arcade.load_texture("images/observatory_back.png")
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

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
        self.click_sound.play(volume=0.5)

class ObjectsView(arcade.View):
    def on_show(self):
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text("What can each instrument see?", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 +25,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("These objects can be seen with similar instruments on or around August 13th, 2020 (in Clinton NY)",
                                                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                                 arcade.color.BLACK, font_size=12, anchor_x="center")
        arcade.draw_text("Binoculars = Ursa Minor Constellation (Little Dipper)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Small Reflector= Moon Surface (Third Quarter)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Large Refractor= M45 Open Cluster (Pleiades)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Observatory= Jupiter and Satellites Ganymede, Europa, & Callisto",
                                            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 125,
                                            arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("[Click to return]", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-150,
                         arcade.color.BLACK, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):

        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)
        self.click_sound.play(volume=0.5)

class InstructionsView(arcade.View):

    def on_show(self):
        self.click_sound = arcade.load_sound("sounds/clicksound.mp3")

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text("Instructions", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Use the corresponding keys to view each celestial object:", SCREEN_WIDTH / 2,
                                           SCREEN_HEIGHT / 2-25, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("B= Binoculars (lowest power,  magnifies highly visible objects)", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 50, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("T= Small Reflector (low power, goes beyond naked eye)", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 75, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("R= Large Refractor (high power, surpasses casual observation)", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 100, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("O= Observatory (highest power, the farthest most can see from Earth)", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 125, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Press Escape to end", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 150, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("[Click to return]", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 185, arcade.color.BLACK, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)
        self.click_sound.play(volume=0.5)

class EndView(arcade.View):
    def on_show(self):
        for sound in self.sound_list:
            arcade.stop_sound(sound)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.NAVY_BLUE)
        arcade.draw_text("Clear skies, thanks for playing!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Peter Butler, June 2020", 700, 25,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.end = True

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()