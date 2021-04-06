from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.behaviors import ToggleButtonBehavior as TB
from kivy.config import Config
from kivy.utils import platform 
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup 
from kivy.uix.button import Button
import os, sys
from kivy.resources import resource_add_path, resource_find
from game_logic.utils import get_path

""" 
Builder is used to load in the design .kv files

platform is used to determine the os:
    A string identifying the current operating system. It is one of: ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’.
"""

# Desktop config
if platform in ["win", "macosx", "linux"]:
    Config.set('graphics', 'resizable', True)
    # fix the width and height of the window  
    Config.set('graphics', 'width', '500') 
    Config.set('graphics', 'height', '500') 
    
# Mobile config
if platform in ["ios","android"]:
    pass
    
# print("We are at", os.getcwd())
# Load in gui 
Builder.load_file(get_path("design/gui.kv"))
Builder.load_file(get_path("design/tiktactoe.kv"))
Builder.load_file(get_path("design/connect4.kv"))
Builder.load_file(get_path("design/dotsandboxes.kv"))

# Import the Screens for the individual games
from game_logic.dotsandboxes import DotsAndBoxesScreen
from game_logic.tiktactoe import TicTacToeScreen
from game_logic.connect4 import Connect4Screen

# Main window screen
class TitleScreen(Screen):
    diff_choice = StringProperty()
    game_choice = StringProperty()
    match_style = StringProperty()
    
    def load_game(self):
        """Function to swap to the game screen and pass the game variables to the appropriate screen. Displays an error message if any of the settings are not selected
        """
        # Show error message if any of the toggles are not picked        
        if not self.diff_choice or not self.game_choice or not self.match_style:
            content = Button(text="Dismiss")
            error = Popup(title="Select one of each option", content=content, size=(40, 60))
            content.bind(on_press=error.dismiss)
            error.open()
            return
        
        # load game settings and swap screens
        game_screen = self.manager.get_screen(self.game_choice)
        game_screen.load_settings(self.diff_choice, self.match_style)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.game_choice

# Class to manage all the screens and load the homescreen
class RootWidget(ScreenManager):
    pass

class GameApp(App):
    title = "Reinforcement Learning Game"
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # This if statement adds the temporary file location to the relative path of the resources (images, .kv, etc)
        resource_add_path(os.path.join(sys._MEIPASS))
    GameApp().run()