import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Interactive Nighttime Observation Game'

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
        arcade.draw_text("Summer of Code 2020", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("(Click to begin)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
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

        self.button_list = []
        self.click_sound = None
        self.end = False


    def setup(self):
        # sounds

        self.back_music = arcade.load_sound("sounds/back_tester.mp3")

        #background image
        self.background = arcade.load_texture("images/background.jpg")

        #hamilton logo?


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

        pass

    def on_mouse_release(self, x, y, button, key_modifiers):

        pass

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()