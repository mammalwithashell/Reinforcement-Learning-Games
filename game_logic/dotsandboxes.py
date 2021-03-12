from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Ellipse
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty

class DotsAndBoxesScreen(Screen):
    score = NumericProperty()
    ai_score = NumericProperty()
    game_grid = ObjectProperty(None)
    difficulty_setting = StringProperty("")
    match = StringProperty("")
    turn = BooleanProperty(True)
    def setup(self):
        with self.game_grid.canvas:
            # Ellipse(pos=(30,30), size=(10,10))
            dot_radius = 10
            for x in range(20, 481, 230):
                for y in range(20, 421, 200):
                    Ellipse(pos=(x - dot_radius, y - dot_radius), size=(dot_radius, dot_radius))

                    
    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        
    def load_settings(self, diff, match):
        self.difficulty_setting = diff
        self.match = match
    