# Authors: Nikki Meyer and Brian Little
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.button import Button
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.resources import resource_find

import random as rand
from .tictactoeAI.BoardEnvironment import BoardEnvironment
from .tictactoeAI.Agent import Agent
from .tictactoeAI.LeagueEnvironment import LeagueEnvironment


def select_difficulty(auto=False):
    x = 0
    diffdict = {
        1: r"game_logic/tictactoeAI/qtables/easy.txt",
        2: r"game_logic/tictatoeAI/qtables/medium.txt",
        3: r"game_logic/tictactoeAI/qtables/hard.txt",
    }
    if not auto:
        while x > 3 or x < 1:
            print("Select a difficulty:")
            print("1: Easy")
            print("2: Medium")
            print("3: Hard")
            x = int(input())

    else:
        x = rand.randint(1, 3)

    return diffdict[x]


class TicTacToeSquare(ButtonBehavior, Image):
    """Custom widget inheriting from both ButtonBehavior and Image objects. These are placed in the design/tictactoe.kv file

    Args:
        ButtonBehavior (kivy.uix.ButtonBehavior): Adds on_press and on_release behavior to other widgets
        Image (kivy.uix.Image): Image widget
    """

    button_number = NumericProperty()

    def __init__(self, **kwargs):
        super(TicTacToeSquare, self).__init__(**kwargs)
        # this could have been done in the kv file and kinda violates mvc
        self.source = resource_find("images/tictactoe/blank.png")


class TicTacToeScreen(Screen):
    """Screen object to be managed by ScreenManager object

    Args:
        Screen (kivy.uix.screenmanager.Screen): This inherits from kivy.relativelayout.RelativeLayout and uses that object's placement system. In the design file we used a gridlayout overwrite that placement system.

        The Object Property type lets kivy objects share variable names with the .kv files.
    """

    main_menu = ObjectProperty(None)
    scoreboard = ObjectProperty(None)
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
    user_data = ObjectProperty(None)
    ai_data = ObjectProperty(None)

    # ----------------------------------------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        self.reset_game()
        return super().on_pre_leave(*args)

    def load_settings(self, diff, match):

        self.difficulty_setting = diff
        self.match = match
        self.board_env = BoardEnvironment(self)
        agent = Agent(self.board_env, diff)
        self.league = LeagueEnvironment(self.board_env, self)
        self.first_league_run = True
        if self.match == "Single Match":
            self.board_env.set_players(agent)
            self.board_env.reset()
            self.scorebox.size_hint_x = 0
            # self.scorebox.text += f"Difficulty Setting: {diff}"

        else:
            self.first_league_run = True
            self.board_env.set_players(agent)

            player_names = []
            board_agents = []
            league_agents = []

            player_names.append("learning strategy and tactics")
            board_agents.append(agent)
            league_agents.append(
                Agent(
                    self.league,
                    "league",
                    "max",
                )
            )

            """player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, resource_find(select_difficulty(True)), 'max'))
            league_agents.append(Agent(self.league, resource_find('game_logic/tictactoeAI/qtables/league.txt'), 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, resource_find(select_difficulty(True)), 'random'))
            league_agents.append(Agent(self.league, resource_find('game_logic/tictactoeAI/qtables/league.txt'), 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, resource_find(select_difficulty(True)), 'random'))
            league_agents.append(Agent(self.league, resource_find('game_logic/tictactoeAI/qtables/league.txt'), 'random'))"""
            self.league.set_players(player_names, league_agents, board_agents)
            self.reset_game()
            self.league.play_pair(self.first_league_run)
            self.first_league_run = False

    # ----------------------------------------------------------------------------------------------------------
    def press_main(self):
        self.reset_game()
        self.match = ""
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"

    def press(self, num):
        """Function called by the Buttons that act as cells of the tictactoe board. The

        Args:
            num ([type]): [description]
        """
        # can't press button if square number in buttonlist
        if num not in self.buttonlist:
            self.buttonlist.add(num)
            self.board_env.play_game_turn(num)

    def press_bet1(self):
        self.player_bet = "single bet"
        self.player_bet_amount = 1
        self.league.play_pair()

    def press_bet2(self):
        self.player_bet = "double bet"
        self.player_bet_amount = 2
        self.league.play_pair()

    def press_bet3(self):
        self.player_bet = "triple bet"
        self.player_bet_amount = 3
        self.league.play_pair()

    def reset_game(self):
        for button in self.square_list:
            button.source = resource_find("images\\tictactoe\\blank.png")
        self.board_env.print_board()
        # clear list of set squares
        self.buttonlist.clear()
        if self.first_league_run:
            self.league.reset_pair()
            self.first_league_run = False

        self.board_env.reset()

    def draw_turn(self, num):
        """Updates the screen based on the user or ai choice"""
        for square_button in self.square_list:
            # if i is
            if square_button.button_number == num:
                square_button.source = (
                    resource_find("images\\tictactoe\\X.png")
                    if self.board_env.turn is "X"
                    else resource_find("images\\tictactoe\\O.png")
                )
                square_button.color = (
                    [0, 1, 0, 1] if self.board_env.turn == "O" else [0, 1, 1, 1]
                )
                self.buttonlist.add(num)
                break

    def winner(self, tie=False):
        """Display winner

        Args:
            tie (bool, optional): Show winner popup. Defaults to False.
        """
        print("Winner Piece: ", self.piece)
        popup = Popup(title="Winner Popup", size_hint=(0.6, 0.4))

        if tie:
            text = "Tie Game"
            winner = True
        elif self.board_env.turn == self.piece:
            # Player is the winner
            winner = True
            text = "You won!"
        else:
            winner = False
            text = "You Lost!"

        # if not league match, display winner and move on
        if self.match != "League Match":
            content = Button(text=text)
            self.board_env.print_board()
            content.bind(on_press=popup.dismiss)
        else:
            content = Button(text=text)

            def play_on(pop_up_self):
                """functionality of button that shows at the end of a league Game

                Args:
                    pop_up_self (Button): This argument is the "self" call for the button we are binding the function to
                """
                self.league.play_pair_pt_2(winner, tie=tie)
                self.reset_game()
                self.league.play_pair(self.first_league_run)
                popup.dismiss()

            content.bind(on_press=play_on)
        popup.add_widget(content)
        popup.open()

    def bet_options(self, options, message, AI_choice, cols=1):
        """Function to display betting options in the league Game

        Args:
            options (list): [description]
            message (str): [description]
            AI_choice (int): [description]
            cols (int, optional): [description]. Defaults to 1.

        """
        # creating grid for popup menu
        content = GridLayout(cols=cols, padding=50, spacing=50)
        # returning early if no options were passed to this function
        if len(options) == 0:
            return False
        # adding a button for each option with the option's text
        for option in options:
            content.add_widget(Button(text=option))
        # creating a popup with 'message' and 'content'
        option_popup = Popup(
            title=message, content=content, size_hint=(0.8, 0.9), auto_dismiss=False
        )
        # function that will be called when a button is clicked
        def option_button(inner_self):
            # dismiss popup
            option_popup.dismiss()
            # grabbing the selected option
            result = inner_self.text
            # calling 'func' with the selected option and the AI's option
            self.league.play_pair_pt_1_5(result, AI_choice)

        # binding option_button button to each option
        for child in content.children:
            child.bind(on_press=option_button)
        # opening popup
        option_popup.open()

    def series_end(self, message):
        """Called when league series ends and displays final league betting information

        Args:
            message (str): Message sent by LeagueEnvironment with final betting info
        """
        content = GridLayout(cols=1, padding=50, spacing=50)
        content.add_widget(Button(text="Play again"))
        content.add_widget(Button(text="Return to menu"))
        series_end_popup = Popup(
            title=message, content=content, size_hint=(0.8, 0.6), auto_dismiss=False
        )
        self.first_league_run = True

        def play_again_button(inner_self):
            series_end_popup.dismiss()
            self.reset_game()
            self.league.play_pair(True)

        def end_game_button(inner_self):
            series_end_popup.dismiss()
            self.press_main()

        content.children[1].bind(on_press=play_again_button)
        content.children[0].bind(on_press=end_game_button)
        series_end_popup.open()
