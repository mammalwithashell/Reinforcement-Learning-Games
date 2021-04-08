from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.popup import Popup 
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout

from kivy.resources import resource_find
from .utils import get_path

import random as rand
import copy
import time
import threading

# Gameplay opponent
from .connect4AI.Agent import Agent

# Board game environment
from .connect4AI.BoardEnvironment import BoardEnvironment

# League betting environment
from .connect4AI.LeagueEnvironment import LeagueEnvironment

# Kivy class that manages Connect4 visuals
class Connect4Screen(Screen):

    # Kivy objects
    # Grid that holds connect4 pieces
    board_grid = ObjectProperty(None)
    # Buttons that user clicks to place pieces
    button_one = ObjectProperty(None)
    button_two = ObjectProperty(None)
    button_three = ObjectProperty(None)
    button_four = ObjectProperty(None)
    button_five = ObjectProperty(None)
    
    # Scoreboard for league betting
    scoreboard = ObjectProperty(None)
    # User half of scoreboard
    user_data = ObjectProperty(None)
    # AI half of scoreboard
    ai_data = ObjectProperty(None)

    '''
        description
            displays a popup menu for selecting betting options. this function
            allows the LeagueEnvironment class to get input from the user

        parameters
            options: list of text options for popup menu
            message: text that will display at top of popup menu
            func: a function that will be called with the selected option
            AI_choice: the AI's choice for this turn is passed to 'func'
                with the User's choice
            cols: number of columns for the popup menu
    '''
    def bet_options(self, options, message, func, AI_choice, cols=1):
        # creating grid for popup menu
        content = GridLayout(cols=cols, padding=100, spacing=50)
        # returning early if no options were passed to this function
        if len(options) == 0:
            return False
        # adding a button for each option with the option's text
        for option in options:
            content.add_widget(Button(text=option))
        # creating a popup with 'message' and 'content'
        option_popup = Popup(title=message, content=content, size_hint=(.8, .9), auto_dismiss=False)
        # function that will be called when a button is clicked
        def option_button(inner_self):
            # dismiss popup
            option_popup.dismiss()
            # grabbing the selected option
            result = inner_self.text
            # calling 'func' with the selected option and the AI's option
            func(result, AI_choice)
        # binding option_button button to each option
        for child in content.children:
            child.bind(on_press=option_button)
        # opening popup
        option_popup.open()

    '''
        deescription
            the connect4 game's setup function
        parameters
            diff: the difficulty selected at the main menu
            match: the type of game being played (single or league)
    '''
    def load_settings(self, diff=None, match=None, reset=False):
        if not diff and not match:
            diff = self.chosen_difficulty
            match = self.match_type

        self.match_type = match

        # creating and saving board environment that will be used for the
        # duration of the game
        if reset:
            self.board_env.reset()
        else:
            self.board_env = BoardEnvironment(self)

        # setting up league match
        if self.match_type == 'League Match':
            self.first_league_run = True

            if reset == False:
                # creating league environment that will be used for the duration of 
                # the game
                league = LeagueEnvironment(self.board_env, self)

                # these three arrays will hold the four possible sets of agents
                # each set has a name, board agent, and league agent
                player_names = []
                board_agents = []
                league_agents = []

                league_qtable = 'game_logic/connect4AI/qtables/league.txt'
                league_qtable = get_path(league_qtable)

                player_names.append('learning strategy and tactics')
                board_agents.append(Agent(self.board_env, resource_find(self.select_difficulty(diff)), 'max'))
                league_agents.append(Agent(league, league_qtable, 'max'))

                '''player_names.append('learning tactics only')
                board_agents.append(Agent(self.board_env, resource_find(self.auto_select_difficulty()), 'max'))
                league_agents.append(Agent(league, league_qtable, 'random'))

                player_names.append('learning strategy only')
                board_agents.append(Agent(self.board_env, resource_find(self.auto_select_difficulty()), 'random'))
                league_agents.append(Agent(league, league_qtable, 'max'))

                player_names.append('no learning')
                board_agents.append(Agent(self.board_env, resource_find(self.auto_select_difficulty()), 'random'))
                league_agents.append(Agent(league, league_qtable, 'random'))'''

                # saving names, league agents, and board agents to 'league'
                league.set_players(player_names, league_agents, board_agents)
                # saving 'league' to this class
                self.league_env = league
            # making betting scoreboard visible
            '''self.scoreboard.size_hint_y = None
            self.scoreboard.height = 200'''
            '''for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 200'''
        # setting up single game
        else:
            # hiding betting scoreboard
            self.scoreboard.size_hint_x = None
            self.scoreboard.width = 0
            
            for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 0
                child.text = ""

        # 2D array that holds the location of connect4 pieces
        self.board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]

        # starting connect4 gameplay
        self.start_game(diff, reset)

    '''
        description
            main function that controls gameplay
        parameters
            num: the user's choice
    '''
    def play_game(self, num=None):
        # returns the winning player or None if there is a tie game
        if (not self.board_env.is_full()):

            # ************ HUMAN-PLAYABLE MODIFICATION
            # AI selects its move
            if(self.board_env.current_player):
                choice = self.board_env.playerA.select_action(self.board_env.board)
            # User selects their move
            else:
                choice = self.board_env.get_lowest_column(num)
            # *********************************************

            # placing the current player's piece in their chosen location
            self.board_env.board[choice] = self.board_env.turn 
            # disabling and hiding buttons for unavailable actions
            self.board_env.available_actions(True)
            # redrawing game board
            self.board_env.kivy_obj.redraw_board()

            # check if current player just won the game
            if self.board_env.winner(self.board_env.turn):
                self.game_end()
                return True
            # handling tie game
            elif self.board_env.is_full(): 
                self.game_end(True)

            # switch players
            self.board_env.turn = 'X' if self.board_env.turn == 'O' else 'O' # switch turn
            self.board_env.current_player = self.board_env.other_player()
            return False
        # it's a tie
        return None

    '''
        description
            begins connect4 game
        parameters
            diff: difficulty of game
    '''
    def start_game(self, diff, reset=False):
        # saving difficulty of game
        self.chosen_difficulty = diff

        # if this is a league match, calling betting functionality
        if self.match_type == 'League Match':
            self.league_env.play_pair(self.first_league_run)
            self.first_league_run = False

        # creating gameplay agent with difficulty 'diff'
        if not reset:
            A = Agent(self.board_env, resource_find(self.select_difficulty(diff)))
            self.gameplay_agent = A
        else:
            self.gameplay_agent.reset_past()

        # 'set_players' will return True if AI has the first turn
        # if True, allowing AI to make first move
        if self.board_env.set_players(self.gameplay_agent):
            self.piece = 'O'
            self.opponent = 'X'
            self.play_game()
        # else, just updating the board display
        else:
            self.piece = 'X'
            self.opponent = 'O'
            self.redraw_board()

        # unhiding any disabled buttons
        self.board_env.available_actions(True)

    '''
        returns qtable for input difficulty 'diff'
    '''
    def select_difficulty(self, diff):
        diffdict = {'Easy': r'game_logic/connect4AI/qtables/easy.txt',
                    'Medium': r'game_logic/connect4AI/qtables/medium.txt',
                    'Hard': r'game_logic/connect4AI/qtables/hard.txt'}
        return diffdict[diff]

    '''
        randomly selecting a difficulty and loading its qtable
    '''
    def auto_select_difficulty(self):
        x = 0
        diffdict = {1: r'game_logic/connect4AI/qtables/easy.txt',
                    2: r'game_logic/connect4AI/qtables/medium.txt',
                    3: r'game_logic/connect4AI/qtables/hard.txt'}

        x = rand.randint(1, 3)
        return diffdict[x]

    '''
        description
            this function is called by the buttons on the gameboard.
            it places a piece in the column selected by the user and 
            allows the AI to place a piece afterwards
        parameters
            num: number corresponding to the column selected by the user
    '''
    def place_piece(self, num):
        # playing user's choice then letting AI play if game isn't over
        result = self.play_game(num)
        if result == False:
            self.play_game()
        return

    '''
        updating board 2D array using board_str
    '''
    def update_board(self):
        board_str = self.board_env.board
        for i in range(0, len(board_str)):
            self.board[4 - int(i / 5)][i % 5] = None if board_str[i] == '-' else board_str[i]

    '''
        updating game board display
    '''
    def redraw_board(self):
        self.update_board()
        # clearing out widgets that made up the previous board display
        self.board_grid.clear_widgets()
        for j in range(0, 5):
            for i in range(0, 5):
                # adding yellow piece if current space belongs to user
                if self.board[4-j][i] == self.piece:
                    self.board_grid.add_widget(Image(source=resource_find("images/connect4/bestchipyellow.png")))
                # adding red piece if current space belongs to AI
                elif self.board[4-j][i] == self.opponent:
                    self.board_grid.add_widget(Image(source=resource_find("images/connect4/bestchipred.png")))
                # adding blank image for empty space
                else:
                    self.board_grid.add_widget(Image(source="", color=(0,0,0)))

    '''
        description
            called when league series ends and displays final league betting info
        parameters
            message: message sent by LeageEnvironment with final betting info
    '''
    def series_end(self, message):
        content = GridLayout(cols=1, padding=100, spacing=50)
        content.add_widget(Button(text="Play again"))
        content.add_widget(Button(text="Return to menu"))
        series_end_popup = Popup(title=message, content=content, size=(40, 60), auto_dismiss=False)
        def play_again_button(inner_self):
            series_end_popup.dismiss()
            self.load_settings(reset=True)
        def end_game_button(inner_self):
            series_end_popup.dismiss()
            self.menu()
        content.children[1].bind(on_press=play_again_button)
        content.children[0].bind(on_press=end_game_button)
        series_end_popup.open()

    '''
        description
            called when game ends and says who won
        parameters
            tie: will be true if this is a tie game
    '''
    def game_end(self, tie=False):
        content = GridLayout(cols=1, padding=100, spacing=50)
        if self.match_type != 'League Match':
            content.add_widget(Button(text="Play again"))
            content.add_widget(Button(text="Return to menu"))
        else:
            content.add_widget(Button(text="Continue"))

        message = "You won!" if self.piece == self.board_env.turn else "You lost :("
        if tie:
            message = "Tie game."
        game_end_popup = Popup(title=message, content=content, size_hint=(.8, .6), auto_dismiss=False)

        # resets the single game
        def play_again_button(inner_self):
            game_end_popup.dismiss()
            # self.load_settings(reset=True)
        # returns user to main menu
        def end_game_button(inner_self):
            game_end_popup.dismiss()
            self.menu()

        # resets game board for next match in league series
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
            self.start_game(self.chosen_difficulty, reset=True)

        if self.match_type == 'League Match':
            content.children[0].bind(on_press=play_on)
            game_end_popup.open()
        else:
            content.children[1].bind(on_press=play_again_button)
            content.children[0].bind(on_press=end_game_button)
            game_end_popup.open()

    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
