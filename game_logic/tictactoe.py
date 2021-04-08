#Authors: Nikki Meyer and Brian Little
import kivy
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup

import random as rand
from os import system
from collections import defaultdict
from .tictactoeAI.BoardEnvironment import BoardEnvironment
from .tictactoeAI.Agent import Agent
from .tictactoeAI.LeagueEnvironment import LeagueEnvironment
from .utils import get_path

def select_difficulty(auto=False):
    x = 0
    diffdict = {1: r'game_logic/tictactoeAI/qtables/easy.txt',
                2: r'game_logic/tictatoeAI/qtables/medium.txt',
                3: r'game_logic/tictactoeAI/qtables/hard.txt'}
    if not auto:
        while(x > 3 or x < 1):
            print("Select a difficulty:")
            print("1: Easy")
            print("2: Medium")
            print("3: Hard")
            x = int(input())

    else:
        x = rand.randint(1, 3)

    return diffdict[x]


class TicTacToeSquare(ButtonBehavior, Image):
    button_number = NumericProperty()
    def __init__(self, **kwargs):
        super(TicTacToeSquare, self).__init__(**kwargs)
        self.source = get_path("images/tictactoe/blank.png")



class TicTacToeScreen(Screen):
    main_menu = ObjectProperty(None)
    scorebox = ObjectProperty(None)
    exit_button = ObjectProperty(None)
    square1 = ObjectProperty(None)
    square2 = ObjectProperty(None)
    square3 = ObjectProperty(None)
    square4 = ObjectProperty(None)
    square5 = ObjectProperty(None)
    square6 = ObjectProperty(None)
    square7 = ObjectProperty(None)
    square8 = ObjectProperty(None)
    square9 = ObjectProperty(None)
    square_list = ListProperty(None)
    bet1 = ObjectProperty(None)
    bet2 = ObjectProperty(None)
    bet3 = ObjectProperty(None)

    buttonlist = set()
    piece = StringProperty(None)
    

#----------------------------------------------------------------------------------------------------------
    

    def load_settings(self, diff, match):

        self.difficulty_setting = diff
        self.match = match
        self.board_env = BoardEnvironment(self)
        agent = Agent(self.board_env, diff)
        self.league = LeagueEnvironment(self.board_env, self)
   

        
        if self.match == "Single Match":
            self.board_env.set_players(agent)
         
            
        else:
            self.reset_betbtns()
            self.first_league_run = True
            self.board_env.set_players(agent)



            player_names = []
            board_agents = []
            league_agents = []

            player_names.append('learning strategy and tactics')
            board_agents.append(Agent(self.board_env, get_path(select_difficulty(True)), 'max'))
            league_agents.append(Agent(self.league, get_path('game_logic/tictactoeAI/qtables/league.txt'), 'max'))

            player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, get_path(select_difficulty(True)), 'max'))
            league_agents.append(Agent(self.league, get_path('game_logic/tictactoeAI/qtables/league.txt'), 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, get_path(select_difficulty(True)), 'random'))
            league_agents.append(Agent(self.league, get_path('game_logic/tictactoeAI/qtables/league.txt'), 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, get_path(select_difficulty(True)), 'random'))
            league_agents.append(Agent(self.league, get_path('game_logic/tictactoeAI/qtables/league.txt'), 'random'))

            self.league.set_players(player_names, league_agents, board_agents)
            



#----------------------------------------------------------------------------------------------------------
    def press_main(self):
        self.match = ''
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        self.reset_game()

    
    def press(self, num):
        #can't press button if square number in buttonlist
        if num not in self.buttonlist:
            self.buttonlist.add(num)
            self.board_env.play_game_turn(num)
    
    def press_bet1(self):
        self.player_bet = 'single bet'
        self.player_bet_amount = 1
        self.league.play_pair()
    
    def press_bet2(self):
        self.player_bet = 'double bet'
        self.player_bet_amount = 2
        self.league.play_pair()
    
    def press_bet3(self):
        self.player_bet = 'triple bet'
        self.player_bet_amount = 3
        self.league.play_pair()
    
    def reset_game(self):
        self.board_env.reset()
        for button in self.square_list:
            button.source = get_path("images\\tictactoe\\blank.png")
        self.board_env.print_board()
        self.buttonlist.clear()
        if (self.match == "League Match"):
            self.league.reset_pair()
    
    def draw_turn(self, num):
        """Updates the screen based on the user or ai choice
        """
        for square_button in self.square_list:
                # if i is 
                if square_button.button_number == num:
                    square_button.source = get_path("images\\tictactoe\\X.png") if self.board_env.turn is "X" else get_path("images\\tictactoe\\O.png")
                    square_button.color = [0, 1, 0, 1] if self.board_env.turn == "O" else [0, 1, 1, 1]
                    self.buttonlist.add(num)
                    break

   
    
    def reset_betbtns(self):
        self.bet1.disabled = False
        self.bet1.background_color = [0.9, 0.9, 0.9, 1]
        self.bet1.color = [1, 1, 1, 1]
        self.bet2.disabled = False
        self.bet2.background_color = [0.9, 0.9, 0.9, 1]
        self.bet2.color = [1, 1, 1, 1]
        self.bet3.disabled = False
        self.bet3.background_color = [0.9, 0.9, 0.9, 1]
        self.bet3.color = [1, 1, 1, 1]
        
    """def winner(self):
        popup = Popup(title="Winner")
        if """
