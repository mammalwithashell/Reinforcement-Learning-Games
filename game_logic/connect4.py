from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button, ButtonBehavior
from kivy.graphics import *
from kivy.uix.popup import Popup 
from kivy.core.window import Window
from kivy.uix.image import Image
from os import system
from kivy.uix.gridlayout import GridLayout

import random as rand
import copy
import numpy as np
import time
import threading
from collections import defaultdict

from .connect4AI.Agent import Agent
from .connect4AI.BoardEnvironment import BoardEnvironment
from .connect4AI.LeagueEnvironment import LeagueEnvironment

def select_difficulty(auto=False):
    x = 0
    diffdict = {1: r'game_logic/connect4AI/qtables/easy.txt',
                2: r'game_logic/connect4AI/qtables/medium.txt',
                3: r'game_logic/connect4AI/qtables/hard.txt'}
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


class Connect4Screen(Screen):
    board_grid = ObjectProperty(None)
    button_one = ObjectProperty(None)
    button_two = ObjectProperty(None)
    button_three = ObjectProperty(None)
    button_four = ObjectProperty(None)
    button_five = ObjectProperty(None)
    
    scoreboard = ObjectProperty(None)
    user_data = ObjectProperty(None)
    ai_data = ObjectProperty(None)

    def bet_options(self, options, message, func, AI_choice, cols=1):
        print("HEY")
        content = GridLayout(cols=cols)
        if len(options) == 0:
            return False
        for option in options:
            content.add_widget(Button(text=option))
        option_popup = Popup(title=message, content=content, size=(40, 60), auto_dismiss=False)
        def option_button(inner_self):
            option_popup.dismiss()
            result = inner_self.text
            func(result, AI_choice)
            #wait_event.set()
        for child in content.children:
            child.bind(on_press=option_button)
        option_popup.open()


    
    def load_settings(self, diff, match):
        print(self, diff, match)
        self.match_type = match
        self.board_env = BoardEnvironment(self)

        if self.match_type == 'League Match':
            self.first_league_run = True
            league = LeagueEnvironment(self.board_env, self)

            player_names = []
            board_agents = []
            league_agents = []

            player_names.append('learning strategy and tactics')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/connect4AI/qtables/league.txt', 'max'))

            player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/connect4AI/qtables/league.txt', 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/connect4AI/qtables/league.txt', 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/connect4AI/qtables/league.txt', 'random'))

            league.set_players(player_names, league_agents, board_agents)
            self.league_env = league
            self.scoreboard.size_hint_y = None
            self.scoreboard.height = 200
            for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 200
        else:
            self.scoreboard.size_hint_y = None
            self.scoreboard.height = 0
            for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 0
                child.text = ""


        self.board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]
        self.start_game(diff)

    def play_game(self, num=None):
        # returns the winning player or None if a tie
        print(self.board_env.is_full())
        if (not self.board_env.is_full() ):

            # ************ HUMAN-PLAYABLE MODIFICATION
            if(self.board_env.current_player):
                choice = self.board_env.playerA.select_action(self.board_env.board)
            else:
                #print("Your board piece is ", self.board_env.turn)
                #print("Select a board piece from the options below:")
                movelist = self.board_env.available_actions()
                self.board_env.print_options()
                #x = int(input())
                x = num + 1
                while(x < 1 or x > 5 or (x-1) not in movelist):
                    print("Invalid choice. Please select another board piece.")
                    x = int(input())
                print()
                choice = self.board_env.get_lowest_column(int(x) - 1)
            # *********************************************



            self.board_env.board[choice] = self.board_env.turn # should check if valid
            self.board_env.available_actions(True)
            self.board_env.kivy_obj.redraw_board_opt_2()
            if self.board_env.winner(self.board_env.turn):
                #self.board_env.print_board()
                print(self.board_env.turn, "won!")
                self.game_end()
                return "You won!" if self.piece == self.board_env.turn else "You lost :("
            elif self.board_env.is_full(): 
                # tie game
                self.game_end(True)

            # switch players
            self.board_env.turn = 'X' if self.board_env.turn == 'O' else 'O' # switch turn
            self.board_env.current_player = self.board_env.other_player()
            return False
        # it's a tie
        return None

    def start_game(self, diff):
        self.chosen_difficulty = diff

        if self.match_type == 'League Match':
            self.league_env.play_pair(self.first_league_run)
            #popup_options(['Return to menu'], "Game over")
            self.first_league_run = False

        A = Agent(self.board_env, self.select_difficulty(diff))

        if self.board_env.set_players(A):
            self.piece = 'O'
            self.opponent = 'X'
            self.play_game()
        else:
            self.piece = 'X'
            self.opponent = 'O'
            self.redraw_board_opt_2()

        # running this to unhide any disabled buttons
        self.board_env.available_actions(True)

    def select_difficulty(self, diff):
        diffdict = {'Easy': r'game_logic/connect4AI/qtables/easy.txt',
                    'Medium': r'game_logic/connect4AI/qtables/medium.txt',
                    'Hard': r'game_logic/connect4AI/qtables/hard.txt'}
        return diffdict[diff]

    def place_piece(self, num, player):
        # playing user's choice then letting AI play if game isn't over
        result = self.play_game(num)
        if result == False:
            self.play_game()
        else:
            print(result)
        return False

    def update_board(self):
        board_str = self.board_env.board
        print(board_str)
        for i in range(0, len(board_str)):
            self.board[4 - int(i / 5)][i % 5] = None if board_str[i] == '-' else board_str[i]

    def redraw_board_opt_2(self):
        self.update_board()
        self.board_grid.clear_widgets()
        for j in range(0, 5):
            for i in range(0, 5):
                if self.board[4-j][i] == self.piece:
                    self.board_grid.add_widget(Image(source="images/connect4/bestchipyellow.png"))
                elif self.board[4-j][i] == self.opponent:
                    self.board_grid.add_widget(Image(source="images/connect4/bestchipred.png"))
                else:
                    self.board_grid.add_widget(Image(source="", color=(0,0,0)))

    def redraw_board(self):
        self.update_board()
        circle_width = Window.size[0] / 5
        for j in range(0, 5):
            for i in range(0, 5):
                with self.board_grid.canvas:
                    Color(1,1,1)
                    if self.board[j][i] == self.piece:
                        Color(1,1,0)
                        Ellipse(source="images/connect4/bestchipyellow.png", pos=(i * circle_width + circle_width / 6, j * circle_width * 0.75 + circle_width / 6), size=(circle_width* 2/3, circle_width * 2/3))
                    elif self.board[j][i] == self.opponent:
                        Color(1,0,0)
                        Ellipse(source="images/connect4/bestchipred.png", pos=(i * circle_width + circle_width / 6, j * circle_width * 0.75  + circle_width / 6), size=(circle_width* 2/3, circle_width * 2/3))
                    else:
                        Ellipse(pos=(i * circle_width + circle_width / 6, j * circle_width * 0.75  + circle_width / 6), size=(circle_width* 2/3, circle_width * 2/3))
                    #Line(circle=(i * circle_width + circle_width/2, j * circle_width + circle_width / 2, circle_width/2))
    
    def series_end(self, message):
        content = GridLayout(cols=1)
        content.add_widget(Button(text="Return to menu"))
        series_end_popup = Popup(title=message, content=content, size=(40, 60), auto_dismiss=False)
        def end_game_button(inner_self):
            series_end_popup.dismiss()
            self.menu()
        content.children[0].bind(on_press=end_game_button)
        series_end_popup.open()

    def game_end(self, tie=False):
        content = GridLayout(cols=1)
        if self.match_type != 'League Match':
            content.add_widget(Button(text="Return to menu"))
        else:
            content.add_widget(Button(text="Continue"))

        message = "You won!" if self.piece == self.board_env.turn else "You lost :("
        if tie:
            message = "Tie game."
        game_end_popup = Popup(title=message, content=content, size=(40, 60), auto_dismiss=False)
        def end_game_button(inner_self):
            game_end_popup.dismiss()
            self.menu()

        def play_on(inner_self):
            self.league_env.play_pair_pt_2(self.piece == self.board_env.turn, tie=tie)
            game_end_popup.dismiss()
            self.board = [
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
            ]
            self.start_game(self.chosen_difficulty)

        if self.match_type == 'League Match':
            content.children[0].bind(on_press=play_on)
            game_end_popup.open()
        else:
            content.children[0].bind(on_press=end_game_button)
            game_end_popup.open()

    def menu(self):
        self.manager.current = "title"