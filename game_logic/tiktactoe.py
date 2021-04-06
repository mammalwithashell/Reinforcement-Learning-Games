#Authors: Nikki Meyer and Brian Little
import kivy
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty

import random as rand
from os import system
from collections import defaultdict
from .tictactoeAI.BoardEnvironment import BoardEnvironment
from .tictactoeAI.Agent import Agent
from .tictactoeAI.LeagueEnvironment import LeagueEnvironment


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
    secondlast_button = ObjectProperty(None)
    massage_box = ObjectProperty(None)
    last_button = ObjectProperty(None)

    buttonlist = []
    square_number = 0
    turn = 1
    

#----------------------------------------------------------------------------------------------------------
    
    def load_settings(self, diff, match):

        self.difficulty_setting = diff
        self.match = match
        self.board_env = BoardEnvironment(self)
        self.board_env.reset()

        if self.match == "Single Match":
            # Set agent difficultiy and assign agent to board
            agent = Agent(self.board_env, diff)
            self.board_env.set_players(agent)
        else:
            self.first_league_run = True
            league = LeagueEnvironment(self.board_env, self)


            player_names = []
            board_agents = []
            league_agents = []

            player_names.append('learning strategy and tactics')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'max'))

            player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'random'))

            league.set_players(player_names, league_agents, board_agents)

 
#----------------------------------------------------------------------------------------------------------
    def press_main(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"

    def press_exit(self):
        self.board_env.board.clear()
        self.buttonlist.clear()
        self.square1.text = '1'
        self.square1.color = [1, 1, 1, 1]
        self.square2.text = '2'
        self.square2.color = [1, 1, 1, 1]
        self.square3.text = '3'
        self.square3.color = [1, 1, 1, 1]
        self.square4.text = '4'
        self.square4.color = [1, 1, 1, 1]
        self.square5.text = '5'
        self.square5.color = [1, 1, 1, 1]
        self.square6.text = '6'
        self.square6.color = [1, 1, 1, 1]
        self.square7.text = '7'
        self.square7.color = [1, 1, 1, 1]
        self.square8.text = '8'
        self.square8.color = [1, 1, 1, 1]
        self.square9.text = '9'
        self.square9.color = [1, 1, 1, 1]
    
    def press(self, num):
        self.turn = self.turn + 1
        self.square_number = num
        print(num)
        if ((self.turn % 2) == 0):
            self.x_o = 'X'
        else:
            self.x_o = 'O'
        #can't press button if square number in buttonlist
        if (self.square_number not in self.buttonlist):
            self.buttonlist.append(int(self.square_number))
            if (int(self.square_number) == 1):
                #self.square1.disabled = True
                self.square1.text = self.x_o
                if (self.x_o == 'X'):
                    self.square1.color = [0, 1, 0, 1]
                else:
                    self.square1.color = [0, 1, 1, 1]
                #https://www.december.com/html/spec/colorrgbadec.html 
            if (int(self.square_number) == 2):
                self.square2.text = self.x_o
                if (self.x_o == 'X'):
                    self.square2.color = [0, 1, 0, 1]
                else:
                    self.square2.color = [0, 1, 1, 1]
            if (int(self.square_number) == 3):
                self.square3.text = self.x_o
                if (self.x_o == 'X'):
                    self.square3.color = [0, 1, 0, 1]
                else:
                    self.square3.color = [0, 1, 1, 1]
            if (int(self.square_number) == 4):
                self.square4.text = self.x_o
                if (self.x_o == 'X'):
                    self.square4.color = [0, 1, 0, 1]
                else:
                    self.square4.color = [0, 1, 1, 1]  
            if (int(self.square_number) == 5):
                self.square5.text = self.x_o
                if (self.x_o == 'X'):
                    self.square5.color = [0, 1, 0, 1]
                else:
                    self.square5.color = [0, 1, 1, 1]
            if (int(self.square_number) == 6):
                self.square6.text = self.x_o
                if (self.x_o == 'X'):
                    self.square6.color = [0, 1, 0, 1]
                else:
                    self.square6.color = [0, 1, 1, 1] 
            if (int(self.square_number) == 7):
                self.square7.text = self.x_o
                if (self.x_o == 'X'):
                    self.square7.color = [0, 1, 0, 1]
                else:
                    self.square7.color = [0, 1, 1, 1] 
            if (int(self.square_number) == 8):
                self.square8.text = self.x_o
                if (self.x_o == 'X'):
                    self.square7.color = [0, 1, 0, 1]
                else:
                    self.square7.color = [0, 1, 1, 1]
            if (int(self.square_number) == 9):
                self.square9.text = self.x_o
                if (self.x_o == 'X'):
                    self.square9.color = [0, 1, 0, 1]
                else:
                    self.square9.color = [0, 1, 1, 1]  
            self.board_env.play_game_turn(int(num))
    

    
    def secondlast(self):
        pass
    
    def last(self):
        pass

