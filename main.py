from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ToggleButtonBehavior as TB
from kivy.config import Config
from kivy.utils import platform 


# Desktop config
if platform in ["win", "macosx", "linux"]:
    Config.set('graphics', 'resizable', False)
    # fix the width and height of the window  
    Config.set('graphics', 'width', '500') 
    Config.set('graphics', 'height', '500') 
    
# Mobile config
if platform in ["ios","android"]:
    pass
    
""" 
Builder is used to load in the design .kv files

platform is used to determine the os:
    A string identifying the current operating system. It is one of: ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’.
"""

# 
from game_logic.tiktactoe import TicTacToeScreen
from game_logic.connect4 import Connect4Screen
from game_logic.dotsandboxes import DotAndBoxesScreen

# Load in gui 
Builder.load_file("design/gui.kv")
Builder.load_file("design/tiktactoe.kv")
Builder.load_file("design/connect4.kv")
Builder.load_file("design/dotsandboxes.kv")

class TitleScreen(Screen):
    def load_game(self):
        # get a list of the difficulty toggle buttons
        diff_tb = [t for t in TB.get_widgets('difficulty') if t.state=='down'][0]
        game_tb = [t for t in TB.get_widgets('game') if t.state=='down'][0]
        match_tb = [t for t in TB.get_widgets('match') if t.state=='down'][0]
        
        # load game settings and swap screens
        game_screen = self.manager.get_screen(game_tb.text)
        game_screen.load_settings(diff_tb.text, match_tb.text)
        self.manager.current =  game_tb.text
    
class RootWidget(ScreenManager):
    pass


class GameApp(App):
    title = "Reinforcement Learning Game"
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    GameApp().run()