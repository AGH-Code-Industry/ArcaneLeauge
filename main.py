from kivy import Config, platform
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.relativelayout import RelativeLayout

class MainWidget(RelativeLayout):

    from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, is_desktop

    FPS = 60

    horizontal_lines_number = 3
    horizontal_lines = []

    player = None
    player_x = None
    player_y = None
    player_level = 1
    player_health = 6
    player_missiles =[]

    x_move = 0
    current_level = 1

    minions_number = 30
    first_init = minions_number
    minions = []
    minions_y_level = []

    minions_missiles = []
    time_delay = 0

    current_offset_x = 0
    SPEED_X = 2.5

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_horizontal_lines()
        self.init_minions()
        self.init_player()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / self.FPS)

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.horizontal_lines_number):
                self.horizontal_lines.append(Line())

    def init_player(self):
        with self.canvas:
            Color(1, 0, 0)
            self.player = Ellipse()

    def init_minions(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.minions_number):
                self.minions.append(Ellipse())
                self.minions_y_level.append(None)

    def init_minions_missiles(self):
        with self.canvas:
            Color(0, 1, 0)
            self.minions_missiles.insert(0, Ellipse())

    def init_player_missiles(self):
        with self.canvas:
            Color(1, 1, 0)
            self.player_missiles.insert(0, Ellipse())

    def generate_minions_coordinates(self):
        main_y = self.height / self.horizontal_lines_number
        spacing_factor = 5

        while(self.first_init > 0):
            for i in range(0, self.minions_number):
                random_x = random.randint(0, 100) * self.width * spacing_factor / 100 - spacing_factor * self.width
                random_y = random.randint(0, 3)
                self.minions[i].pos = [random_x, random_y * main_y]
                self.minions_y_level[i] = random_y
                self.first_init -= 1

        for i in range(0, self.minions_number):
            if self.minions[i].pos[0] > self.width:
                random_x = random.randint(0, 100) * self.width * spacing_factor / 100 - spacing_factor * self.width
                random_y = random.randint(0, 3)
                self.minions[i].pos = [random_x, random_y * main_y]
                self.minions_y_level[i] = random_y

    def minions_coordinates_from_index(self, index):
        x, y = self.minions[index].pos
        return x, y

    def minions_missiles_coordinates_from_index(self, index):
        x, y = self.minions_missiles[index].pos
        return x, y

    def player_coordinates(self):
        x, y = self.player.pos
        return x, y

    def update_horizontal_lines(self):
        y_spacing = self.height / self.horizontal_lines_number

        for i in range (0, self.horizontal_lines_number):
           self.horizontal_lines[i].points = (0, y_spacing * (i+1), self.width, y_spacing * (i+1))

    def update_player(self):
        default_x = .9 * self.width
        default_y = self.current_level / 3 * self.height
        player_size = self.height * .12

        self.player.pos = [default_x + self.x_move, default_y ]
        self.player.size = [player_size, player_size]

    def update_minions(self):
        main_y = self.height / self.horizontal_lines_number
        minions_size = 0.1 * self.height
        for i in range(0, self.minions_number):
            self.minions[i].size = [minions_size, minions_size]
            x, y = self.minions_coordinates_from_index(i)
            x += self.SPEED_X
            y = self.minions_y_level[i] * main_y
            self.minions[i].pos = [x, y]

    def update_minions_missiles(self):
        player_x, player_y = self.player_coordinates()
        player_size = 0.12 * self.height

        for missiles in self.minions_missiles:
            x, y = missiles.pos
            x += 2 * self.SPEED_X

            # SUKI ZNIKAJA JAK WYLECA ZA DALEKO ALBO MNIE JEBNA
            if player_x < x < player_x + player_size and player_y < y < player_y + player_size:
                x = 3 * self.width
                self.player_health -= 1

            if x >= 5 * self.width:
                del self.minions_missiles[-1]

            missiles.pos = [x, y]

    def update_player_missiles(self):
        for missiles in self.player_missiles:
            x, y = self.player_coordinates()
            x -= 2 * self.SPEED_X

            if x < 0:
                del self.minions_missiles[-1]

            missiles.pos = [x, y]

# ============================================================================================================================
    def update(self, time_delta):
        # print(self.player_coordinates())
        # print(time_delta)
        self.update_horizontal_lines()
        self.generate_minions_coordinates()
        self.update_minions()
        self.update_player()


        self.current_offset_x += self.SPEED_X
        missiles_size = 0.1 * self.height
#asd
        #MINIONS MISSILES
        if self.time_delay % (self.FPS * 3) == 1:
            for i in range(0, self.minions_number):
                x, y = self.minions_coordinates_from_index(i)
                if x >= 0:
                    self.init_minions_missiles()
                    self.minions_missiles[0].pos = [x, y + 10]
                    self.minions_missiles[0].size = [missiles_size, missiles_size/2]

        self.update_minions_missiles()
        self.update_player_missiles()
        self.time_delay += 1
        print(len(self.minions_missiles))
        # print(self.player_health)
# ============================================================================================================================

class ArcadeLeaugeApp(App):
    pass

ArcadeLeaugeApp().run()