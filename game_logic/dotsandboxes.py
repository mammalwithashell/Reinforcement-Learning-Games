from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Ellipse, Line
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window

class DotsAndBoxesScreen(Screen):
    score = NumericProperty()
    ai_score = NumericProperty()
    game_grid = ObjectProperty(None)
    difficulty_setting = StringProperty("")
    match = StringProperty("")
    turn = BooleanProperty(True)
    dots = ListProperty()
    def setup(self):
        print(Window.size)
        with self.game_grid.canvas:
            # Ellipse(pos=(30,30), size=(10,10))
            dot_radius = 10
            for x in range(20, 481, 230):
                for y in range(20, 421, 200):
                    self.dots.append(Ellipse(pos=(x - dot_radius, y - dot_radius), size=(dot_radius, dot_radius)))
            
    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        
    def load_settings(self, diff, match):
        self.difficulty_setting = diff
        self.match = match
    
    def on_touch_down(self, touch):
        print(touch.x, touch.y)
        if touch.x > 20 and touch.x < 250:
            with self.game_grid.canvas:
                Line(pos=(20, 20, 250, 20))
        return super().on_touch_down(touch)
    
    def on_size(self, instance, value):
        if self.manager.current == self.name:
            self.dots[0].pos = (40, 40)