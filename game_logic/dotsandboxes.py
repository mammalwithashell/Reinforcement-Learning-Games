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
    
    #dots = [self.game_grid.canvas.get_group(f"dot{i}") for i in range(9)]
    
    def setup(self):
        print(Window.size)

            
    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        
    def load_settings(self, diff, match):
        self.difficulty_setting = diff
        self.match = match
    
    def on_touch_down(self, touch):
        print(touch.x, touch.y)
        return super().on_touch_down(touch)
    
    def on_size(self, instance, value):
        self.game_grid.clear_widgets()