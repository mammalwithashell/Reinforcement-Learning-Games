from kivy.uix.screenmanager import Screen
from kivy.graphics import Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
class DotsAndBoxesScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)
        game = BoxLayout(orientation="horizontal")
        self.add_widget(game)
        
        menu = Button(text="Hello")
        menu.bind(on_press=self.menu)
        game.add_widget(menu)
        with game.canvas:
            # Ellipse(pos=(30,30), size=(10,10))
            dot_radius = 10
            for x in range(20, 481, 230):
                for y in range(20, 421, 200):
                    Ellipse(pos=(x - dot_radius, y - dot_radius), size=(dot_radius, dot_radius))
                    
    def menu(self):
        self.manager.current = "title"
        
    def load_settings(self, diff, match):
        pass
    
    def on_touch_down(self, touch):
        pass