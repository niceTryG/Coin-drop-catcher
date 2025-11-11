from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint


class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Window setup
        self.width = Window.width
        self.height = Window.height

        # Assets
        self.wagon_background = "./images/background.png"
        self.food_image = "./images/food.png"
        self.wagon_image = "./images/wagon.png"

        # Game parameters
        self.food_size = 40
        self.wagon_size = (120, 70)
        self.speed = 12
        self.gravity = 3.5
        self.number_of_food = 3       # Level 1: 3 coins
        self.score_level = 20         # Every 20 points -> new level
        self.max_food = 10            # Max number of coins

        # Miss logic: Level 1 -> 3, L2 -> 4, L3 -> 5, ...
        self.level = 1
        self.base_missed = 3          # starting allowed misses at level 1
        self.allowed_missed = self.base_missed

        # Game state
        self.direction = 0
        self.score = 0
        self.missed = 0
        self.foods = []
        self.game_over = False

        # --- Graphics ---
        with self.canvas:
            # Wagon
            self.wagon = Rectangle(
                source=self.wagon_image,
                size=self.wagon_size,
                pos=(self.width / 2 - self.wagon_size[0] / 2, 0)
            )
            
            # Background
            self.background = Rectangle(
                source=self.wagon_background,
                pos=(0, 0),
                size=(self.width, self.height)
            )

            # Initial foods
            for _ in range(self.number_of_food):
                x = randint(0, self.width - self.food_size)
                y = randint(self.height // 2, self.height - self.food_size)
                rect = Rectangle(
                    source=self.food_image,
                    pos=(x, y),
                    size=(self.food_size, self.food_size)
                )
                self.foods.append(rect)


        # --- Labels ---
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos=(10, self.height - 50),
        )

        self.level_label = Label(
            text=f"Level: {self.level}",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos=(220, self.height - 50),
        )

        self.missed_label = Label(
            text=f"Missed: {self.missed}/{self.allowed_missed}",
            font_size=24,
            color=(1, 0.6, 0.6, 1),
            size_hint=(None, None),
            size=(320, 40),
            pos=(430, self.height - 50),
        )

        self.add_widget(self.score_label)
        self.add_widget(self.level_label)
        self.add_widget(self.missed_label)

        # --- Keyboard ---
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        if self.keyboard:
            self.keyboard.bind(on_key_down=self.on_key_down,
                               on_key_up=self.on_key_up)

        # --- Game loop ---
        Clock.schedule_interval(self.update, 1 / 60.0)

    # ---------- Keyboard ----------
    def on_keyboard_closed(self, *args):
        if self.keyboard:
            self.keyboard.unbind(on_key_down=self.on_key_down,
                                 on_key_up=self.on_key_up)
            self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'right':
            self.direction = 1
        elif keycode[1] == 'left':
            self.direction = -1

    def on_key_up(self, keyboard, keycode):
        if keycode[1] in ('right', 'left'):
            self.direction = 0

    # ---------- Main update loop ----------
    def update(self, dt):
        if self.game_over:
            return

        # Move wagon
        wx, wy = self.wagon.pos
        if self.direction == 1:
            wx += self.speed
        elif self.direction == -1:
            wx -= self.speed

        # Keep wagon inside window
        wx = max(0, min(wx, self.width - self.wagon_size[0]))
        self.wagon.pos = (wx, wy)

        # Move foods & check collisions
        for food in self.foods:
            fx, fy = food.pos
            fy -= self.gravity
            food.pos = (fx, fy)

            # If food missed (goes below screen)
            if fy + self.food_size < 0:
                self.missed += 1
                self.update_labels()

                if self.missed >= self.allowed_missed:
                    self.trigger_game_over()
                    return

                # Respawn missed food at top
                fx = randint(0, self.width - self.food_size)
                fy = self.height
                food.pos = (fx, fy)

            # If food caught
            elif self.check_collision(self.wagon, food):
                self.score += 1
                self.update_labels()

                # Respawn caught food at top
                fx = randint(0, self.width - self.food_size)
                fy = self.height
                food.pos = (fx, fy)

                # Level up every score_level points
                if self.score % self.score_level == 0:
                    self.level_up()

    # ---------- Helpers ----------
    def update_labels(self):
        self.score_label.text = f"Score: {self.score}"
        self.level_label.text = f"Level: {self.level}"
        self.missed_label.text = f"Missed: {self.missed}/{self.allowed_missed}"

    def level_up(self):
        # Increase level
        self.level += 1

        # Reset misses
        self.missed = 0

        # Update allowed misses: L1=3, L2=4, L3=5, ...
        self.allowed_missed = self.base_missed + (self.level - 1)

        # Increase falling speed (but not too crazy)
        self.gravity = min(10, self.gravity + 0.8)

        # Add one more coin, up to max_food
        if len(self.foods) < self.max_food:
            x = randint(0, self.width - self.food_size)
            y = self.height
            with self.canvas:
                new_food = Rectangle(
                    source=self.food_image,
                    pos=(x, y),
                    size=(self.food_size, self.food_size)
                )
            self.foods.append(new_food)

        self.update_labels()

    def trigger_game_over(self):
        self.game_over = True

        game_over_label = Label(
            text=f"GAME OVER!\nFinal Score: {self.score}\nLevel Reached: {self.level}",
            font_size=40,
            color=(1, 0.3, 0.3, 1),
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=(self.width, self.height),
            pos=(0, 0),
        )
        self.add_widget(game_over_label)

    def check_collision(self, r1, r2):
        x1, y1 = r1.pos
        w1, h1 = r1.size
        x2, y2 = r2.pos
        w2, h2 = r2.size

        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )


class Main(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    Main().run()
