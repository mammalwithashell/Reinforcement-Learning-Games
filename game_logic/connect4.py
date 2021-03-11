from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.popup import Popup 

import random
import copy
import numpy as np
import time
from collections import defaultdict

class Connect4Screen(Screen):
    board_grid = ObjectProperty(None)
    def load_settings(self, diff, match):
        print(self, diff, match)
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
            self.board_env.kivy_obj.redraw_board()
            if self.board_env.winner(self.board_env.turn):
                self.board_env.print_board()
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

    class BoardEnvironment:
        """ this class creates an environment for agents to interact with"""

        def __init__(self, parent_object):
            "initialize board"
            self.kivy_obj = parent_object
            return

        def set_players(self, playerA):
            " connects players with the environment "
            self.playerA = playerA
            return self.reset() # defines current_player

        def reset(self):
            self.turn = 'X' # the board always starts with X, regardless of which player

            # board states are a 42-character representing the state of the board.
            self.board = list('-------------------------')
            if (self.playerA): # if they are set
                self.playerA.reset_past()
                if (random.random() < 0.5):  # randomly pick the player to start
                    self.current_player = True
                else:
                    self.current_player = False
            return self.current_player

        def print_board(self, board_string = None):
            "print more readable board either from supplied board string or the current board"
            if not board_string:
                B = self.board
            else:
                B = board_string
            
            print(B[0],'|', B[1],'|', B[2],'|',B[3],'|',B[4], sep='')
            # print('-------------')
            print(B[5],'|', B[6],'|', B[7],'|',B[8],'|',B[9], sep='')
            # print('-------------')
            print(B[10],'|', B[11],'|', B[12],'|',B[13],'|',B[14], sep='')
            # print('-------------')
            print(B[15],'|', B[16],'|', B[17],'|',B[18],'|',B[19], sep='')
            # print('-------------')
            print(B[20],'|', B[21],'|', B[22],'|',B[23],'|',B[24], sep='')

        def get_state(self):
            return "".join(self.board)

        def print_options(self):
            temp_board = copy.copy(self.board)
            for col in range(5):
                bottom = self.get_lowest_column(col)
                if(bottom != -1):
                    temp_board[bottom] = col + 1
            self.print_board(temp_board)

        def get_lowest_column(self, i):
            if(self.board[i] == '-'):
                while(i + 5 < 25):
                    if(self.board[i+5] == '-'):
                        i = i + 5
                    else:
                        break
            else:
                return -1
            return i

        def other_player(self):
            # note, returns other player even if playerA is playing itself
            return not self.current_player

        def available_actions(self):
            movelist = []
            for i in range(5):
                if self.board[i] == '-':
                    movelist.append(i)
                else:
                    continue
            return movelist

        def winner(self, turn):
            straight_lines = (
                (0,1,2,3),
                (1,2,3,4),
                    (5,6,7,8),
                    (6,7,8,9),
                    (10,11,12,13),
                    (11,12,13,14),
                    (15,16,17,18),
                    (16,17,18,19),
                    (20,21,22,23),
                    (21,22,23,24),

                    (0,6,12,18),
                    (6,12,18,24),
                    (1,7,13,19),
                    (5,11,17,23),


                    (3,7,11,15),
                    (4,8,12,16),
                    (8,12,16,20),
                    (9,13,17,21),

                (0,5,10,15),
                    (5,10,15,20),
                    (1,6,11,16),
                    (6,11,16,21),
                    (2,7,12,17),
                    (7,12,17,22),
                    (3,8,13,18),
                    (8,13,18,23),
                    (4,9,14,19),
                    (9,14,19,24)
                    )
            #     for turn in check_for:
            for line in straight_lines:
                if all(x == turn for x in (self.board[i] for i in line)):
                    return turn
            return '' # if there is no winner

        def is_full(self):
            return('-' not in self.board)

    class Agent:
        """ this class is a generic Q-Learning reinforcement learning agent for discrete states and fixed actions
        represented as strings"""
        def __init__(self, environment, difficulty):
            self.environment = environment
            tempdict = ''
            with open(difficulty, 'r') as f:
                for i in f.readlines():
                    tempdict = i
            tempdict = eval(tempdict)
            self.Q = defaultdict(lambda: 0.0, tempdict)
            self.reset_past()

        def reset_past(self):
            self.past_action = None
            self.past_state = None

        def select_action(self, states):
            print("AI select")
            available_actions = self.environment.available_actions()
            Q_vals = [self.Q[(self.environment.get_state(), x)] for x in available_actions]
            #randomly pick one of the maximum values
            max_val = max(Q_vals) # will often be 0 in the beginning
            max_pos = [i for i, j in enumerate(Q_vals) if j == max_val]
            max_indices = [available_actions[x] for x in max_pos]
            choice = random.choice(max_indices)
            self.past_state = self.environment.get_state()
            self.past_action = choice

            while(choice + 5 < 25):
                if(self.environment.board[choice+5] == '-'):
                    choice = choice + 5
                else:
                    break

            return choice


    def start_game(self, diff):
        self.board_env = self.BoardEnvironment(self)
        A = self.Agent(self.board_env, self.select_difficulty(diff))

        if self.board_env.set_players(A):
            self.piece = 'O'
            self.opponent = 'X'
            self.play_game()
        else:
            self.piece = 'X'
            self.opponent = 'O'
            self.redraw_board()

    def select_difficulty(self, diff):
        diffdict = {'Easy': r'game_logic/connect4games/easy.txt',
                    'Medium': r'game_logic/connect4games/medium.txt',
                    'Hard': r'game_logic/connect4games/hard.txt'}
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
        
    def redraw_board(self):
        self.update_board()
        circle_width = 1000 / 5
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
    
    def game_end(self, tie=False):
        content = Button(text="Dismiss")
        message = "You won!" if self.piece == self.board_env.turn else "You lost :("
        if tie:
            message = "Tie game."
        game_end_popup = Popup(title=message, content=content, size=(40, 60))
        def bind_to_popup(inner_self):
            game_end_popup.dismiss()
            self.menu()
        content.bind(on_press=bind_to_popup)
        game_end_popup.open()

    def menu(self):
        self.manager.current = "title"