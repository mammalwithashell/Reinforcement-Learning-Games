from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.utils import platform 
from kivy.properties import StringProperty
from kivy.uix.popup import Popup 
from kivy.uix.button import Button
from kivy.resources import resource_add_path, resource_find
# resource_add_path changes where resource_find looks for a file

import os, sys
import cProfile
from mmap import mmap

""" 
Builder is used to load in the design .kv files

platform is used to determine the os:
    A string identifying the current operating system. It is one of: ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’.
"""

# Desktop config
if platform in ["win", "macosx", "linux"]:
    Config.set('graphics', 'resizable', False)
    # fix the width and height of the window  
    Config.set('graphics', 'width', '600') 
    Config.set('graphics', 'height', '800') 
    
# Mobile config
if platform in ["ios","android"]:
    pass
    
def load_qtable(path:str) -> bytes:
    """Read the qtable into memory

    Args:
        path (str): The path to the qtable

    Returns:
        mmap: A readable filepointer that allows us to read faster
    """
    with open(resource_find(path), "r+b") as f:
        mm = mmap(f.fileno(), 0)
        return mm.readline().decode('utf-8')
    
    
# Main window screen
class TitleScreen(Screen):
    diff_choice = StringProperty()
    game_choice = StringProperty()
    match_style = StringProperty()
    
    # Dict of dicts mapping possible game states to appropriate qtable
    qtables = {
        "Tic-Tac-Toe": {
            "Easy": load_qtable("game_logic\\tictactoeAI\\qtables\\easy.txt"),
            "Medium": load_qtable("game_logic\\tictactoeAI\\qtables\\medium.txt"), 
            "Hard": load_qtable("game_logic\\tictactoeAI\\qtables\\hard.txt")
        },
        
        "Connect 4": {
            "Easy": load_qtable("game_logic\connect4AI\qtables\easy.txt"),
            "Medium": load_qtable("game_logic\connect4AI\qtables\medium.txt"), 
            "Hard": load_qtable("game_logic\connect4AI\qtables\hard.txt")
        }, 
        
        "Dots and Boxes": {
            "Easy": load_qtable("game_logic\dotsandboxesAI\qtables\easy.txt"),
            "Medium": load_qtable("game_logic\dotsandboxesAI\qtables\medium.txt"), 
            "Hard": load_qtable("game_logic\dotsandboxesAI\qtables\hard.txt")
        }
    }
    
    
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

# Class to manage all the screens and load the homescreen (intentionally left blank)
class RootWidget(ScreenManager):
    pass

class GameApp(App):
    title = "Reinforcement Learning Game"
    
    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.print_stats()
        
    def build(self):
        return RootWidget()

def main():
    if hasattr(sys, '_MEIPASS'):
        # This if statement adds the temporary file location to the relative path of the resources (images, .kv, etc)
        resource_add_path(os.path.join(sys._MEIPASS))
        
    # Load in gui 
    Builder.load_file(resource_find("design/gui.kv"))
    Builder.load_file(resource_find("design/tiktactoe.kv"))
    Builder.load_file(resource_find("design/connect4.kv"))
    Builder.load_file(resource_find("design/dotsandboxes.kv"))
    
    # Import the Screens for the individual games
    from game_logic.dotsandboxes import DotsAndBoxesScreen
    from game_logic.tiktactoe import TicTacToeScreen
    from game_logic.connect4 import Connect4Screen

    GameApp().run()

if __name__ == '__main__':
    main()