from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Line, Color
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    StringProperty,
    BooleanProperty,
    ListProperty,
)
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.resources import resource_find

import random as rand

# Import AI stuff
from .dotsandboxesAI.BoardEnvironment import BoardEnvironment
from .dotsandboxesAI.Agent import Agent
from .dotsandboxesAI.LeagueEnvironment import LeagueEnvironment
from time import sleep


def select_difficulty(auto=False):
    x = 0
    diffdict = {
        1: r"game_logic/dotsandboxesAI/qtables/easy.txt",
        2: r"game_logic/dotsandboxesAI/qtables/medium.txt",
        3: r"game_logic/dotsandboxesAI/qtables/hard.txt",
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


class Dot(Image):
    """Custom widget inheriting from Image object. These are placed in the design/dotsandboxes.kv file

    Args:
        Image (kivy.uix.Image): Image widget
    """

    button_number = NumericProperty()

    def __init__(self, **kwargs):
        super(Dot, self).__init__(**kwargs)
        self.source = resource_find("images/dotsandboxes/dot.png")


class DotsAndBoxesScreen(Screen):
    """Screen object to be managed by ScreenManager object

    Args:
        Screen (kivy.uix.screenmanager.Screen): This inherits from kivy.relativelayout.RelativeLayout and uses that object's placement system. In the design file we used a gridlayout overwrite that placement system.

        The Object Property type lets kivy objects share variable names with the .kv files.
    """

    score = NumericProperty()
    ai_score = NumericProperty()
    game_grid = ObjectProperty(None)
    difficulty_setting = StringProperty("")
    match = StringProperty("")
    turn = BooleanProperty(True)
    piece = StringProperty("")
    lines = []
    dots = ListProperty()
    # dictionary mapping box scores to their image widget
    captured_boxes = []
    scoreboard = ObjectProperty(None)
    user_data = ObjectProperty(None)
    ai_data = ObjectProperty(None)
    first_league_run = True

    # a dictionary mapping dot numbers to acceptable dots to be paired with
    accepted_lines = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 6, 4],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [7, 5],
    }

    # Map dots to lines in the board environment
    actual_lines = {
        (1, 2): 11,
        (0, 1): 10,
        (2, 5): 9,
        (1, 4): 8,
        (0, 3): 7,
        (4, 5): 6,
        (4, 3): 5,
        (5, 8): 4,
        (4, 7): 3,
        (3, 6): 2,
        (8, 7): 1,
        (6, 7): 0,
    }

    start_dot = None

    def on_enter(self, *args):
        """Kivy Screen event listener that is run before the screen is entered

        Returns:
            None: Used to reset the board before entering the screen
        """

        self.clear_game_screen()
        self.board_env.reset()
        return super().on_enter(*args)

    def on_leave(self, *args):
        """Kivy Screen event listener that is run as the screen is left

        Returns:
            None:
        """
        self.restart()
        return super().on_leave(*args)

    def load_settings(self, diff, match):
        """
        Called whenever this screen is loaded
        self.lines is a list of tuples containing
        a line instruction object
        the start dot number
        the end dot number
        """

        self.difficulty_setting = diff
        self.match = match
        agent = Agent(
            resource_find(
                f"game_logic/dotsandboxesAI/qtables/{self.difficulty_setting.lower()}.txt"
            )
        )
        self.board_env = BoardEnvironment(self, agent)
        self.scoreboard.size_hint_y = None

        # Load different settings based on game type
        if self.match == "Single Match":
            self.piece = self.board_env.turn
            if self.piece == "O":
                choice = [
                    i for i, char in enumerate(self.board_env.board) if char == "X"
                ][0]
                self.draw_ai_turn(choice, self.board_env.turn)

            # self.board_env.set_players(agent)
            self.board_env.print_board()
            self.scoreboard.height = 0
            self.ai_data.text, self.user_data.text = "", ""
            self.board_env.reset()
        else:
            # League Match
            self.first_league_run = True
            league = LeagueEnvironment(self.board_env, self)

            player_names = []
            board_agents = []
            league_agents = []

            player_names.append("learning strategy and tactics")
            board_agents.append(agent)
            league_agents.append(
                Agent(
                    resource_find("game_logic/dotsandboxesAI/qtables/league.txt"),
                    league,
                )
            )

            # player_names.append('learning tactics only')
            # board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            # league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'random'))

            # player_names.append('learning strategy only')
            # board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            # league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'max'))

            # player_names.append('no learning')
            # board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            # league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'random'))

            league.set_players(player_names, league_agents, board_agents)
            self.league_env = league
            self.scoreboard.height = 200
            for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 200

            league.play_pair(self.first_league_run)
            self.first_league_run = False

    def menu(self):
        """Swap screen back to title screen"""

        self.clear_game_screen()
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"

    def restart(self):
        """This function is run whenever the "Restart Game" Button is pressed. Also used elsewhere"""
        self.clear_game_screen()
        self.lines = []
        self.board_env.reset()
        self.piece = self.board_env.turn
        self.board_env.print_board()
        self.score, self.ai_score = 0, 0

    def league_restart(self):
        """This function is run whenever the "Restart Game" Button is pressed and the league environment is active"""
        self.clear_game_screen()
        self.lines = []
        self.board_env.reset()
        self.league_env.reset_pair()
        self.league_env.play_pair(True)
        self.piece = self.board_env.turn
        self.board_env.print_board()
        self.score, self.ai_score = 0, 0

    def on_touch_down(self, touch):
        """Kivy event listener that is called when the user clicks in the Window

        Args:
            touch (kivy.MotionEvent): https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent

            This function checks if any dot was clicked

        Returns:
        """
        # find what dot the mouse was over and save it to the start_dot property
        for i, _ in enumerate(self.dots):
            # if touch is within a box twice the radius of the dot, we draw
            if self.dots[i].collide_point(*touch.pos):
                self.start_dot = i
                break
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """kivy event listener that is called when the user lets go of the mouse or their touch

        Args:
            touch (kivy.MotionEvent): https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent

            This function checks if any dot was clicked

        Returns:
        """
        # find what dot the mouse is over on mouse release and draw the appropriate line
        turn = self.board_env.turn
        if self.start_dot is None:
            return super().on_touch_up(touch)

        for dot_index, dot_obj in enumerate(self.dots):
            # if touch is within a box twice the radius of the dot, we draw
            if self.check_for_dot_click(touch, dot_index, dot_obj):
                with self.game_grid.canvas:
                    # save line to lines property to be updated on_size
                    points = list(self.dots[self.start_dot].center) + list(
                        dot_obj.center
                    )
                    # add half dot radius to x and y for the line because the dot position is measured from bottom left corner of dots (the radius of the dot is 10)
                    Color(1, 0, 0) if self.board_env.turn == "X" else Color(0, 0, 1)
                    self.lines.append(
                        (
                            Line(points=points, width=3, group="lines"),
                            self.start_dot,
                            dot_index,
                        )
                    )

                # Add line to board environment
                # try except pairs to return line choice
                try:
                    choice = self.actual_lines[(self.start_dot, dot_index)]
                except KeyError:
                    choice = self.actual_lines[(dot_index, self.start_dot)]

                # play_game_turn returns true if the user scores
                # let ai move if user doesn't score
                if not self.board_env.play_game_turn(choice):
                    # Let AI think
                    sleep(0.5)

                    if not self.board_env.is_full():
                        # Add AI move
                        self.board_env.play_game_turn()
                        self.board_env.print_board()
                    else:
                        self.is_full()

                # if the board is full, display the winner popup
                if self.board_env.is_full():
                    self.is_full()

                # change turn bool
                # self.turn = not self.turn
                self.start_dot = None
        return super().on_touch_up(touch)

    def check_for_dot_click(self, touch, dot_index, dot_obj):
        """Check if the user clicked a second dot valid with the current dot

        Args:
            touch (Touch): Kivy touch object
            dot_index (int): Index of dot we are checking
            dot_obj (kivy.Instruction): The object in memory that represents the dot drawing

        Returns:
            bool: Returns true if the dot that the user lets go of the mouse over is a valid pair with the dot from click
        """

        # warning monster bool
        return (
            self.dots[dot_index].collide_point(*touch.pos)
            and self.start_dot is not None
            and dot_index in self.accepted_lines[self.start_dot]
            and self.check_dot_pair(dot_index, self.start_dot)
            in self.board_env.available_actions()
        )

    def draw_ai_turn(self, choice, turn):
        """Draw the line based on AI turn. This function is called with the board environment method play_game_turn

        Args:
            choice (int): Choice decided by the AI.
        """
        actual_lines = {
            (1, 2): 11,
            (0, 1): 10,
            (2, 5): 9,
            (1, 4): 8,
            (0, 3): 7,
            (4, 5): 6,
            (4, 3): 5,
            (5, 8): 4,
            (4, 7): 3,
            (3, 6): 2,
            (8, 7): 1,
            (6, 7): 0,
        }

        # Reverse the dictionary of lines and dots and find the dots based on the ai choice
        line_choice_dots = {value: key for key, value in actual_lines.items()}
        dots = line_choice_dots[
            choice
        ]  # get the entry in the dictionary that maps the line indexes to the dot indexes

        with self.game_grid.canvas:
            # save line to lines property to be updated on_size
            points = list(self.dots[dots[0]].center) + list(self.dots[dots[1]].center)
            # add half dot radius to x and y for the line because the dot position is measured from bottom left corner of dots (the radius of the dot is 10)
            # The amount added to i should be half of the dot_size set in the dotsandboxes.kv file
            Color(1, 0, 0) if turn == "X" else Color(0, 0, 1)

            line = Line(points=points, width=3, group="lines")
            self.lines.append((line, dots[0], dots[1]))

    def draw_captured_box(self, box_index, turn):

        # map box index to quadrant of grid
        boxes = {
            14: (0, 1, 3, 4),  # bottom left box
            15: (1, 2, 4, 5),  # bottom right box
            13: (4, 5, 8, 7),  # top right box
            12: (4, 3, 6, 7),  # top left box
        }

        avg_x, avg_y = 0, 0
        for dot_index in boxes[box_index]:
            # print(self.dots[dot_index].pos[0], self.dots[dot_index].pos[1])
            avg_x += self.dots[dot_index].center_x
            avg_y += self.dots[dot_index].center_y
        avg_x /= 4
        avg_y /= 4
        # print("Averages", avg_x, avg_y)
        color = "red" if turn == "X" else "blue"
        captured_box = Image(
            source=f"./images/dotsandboxes/{color}_{turn}.png",
            pos_hint={"center_x": avg_x / self.width, "center_y": avg_y / self.height},
        )
        self.captured_boxes.append(captured_box)
        self.add_widget(captured_box)

    def is_full(self):
        """Display pop up when the board fills
        Called from within the self.board property of type BoardEnvironment

        Returns:
            None: Pop up that displays end condition of the game
            win
            lose
            tie
        """
        tie = self.ai_score == self.score

        winner_popup = Popup(size_hint=(0.8, 0.9), title="Winner Popup")
        # self.board.score_board is a dictionary of str:int with keys "X" and "O"
        if self.score > self.ai_score:
            text = "You are the winner"
            winner = True
        elif self.ai_score > self.score:
            text = "Computer is the winner"
            winner = False
        else:  # it's a tie
            text = "There was a tie!"
            winner = None

        # if not league match, display winner and move on
        if self.match != "League Match":
            content = Button(text=text)
            self.board_env.print_board()
            content.bind(on_press=winner_popup.dismiss)
        else:
            content = Button(text=text)

            def play_on(pop_up_self):
                """functionality of button that shows at the end of a league Game

                Args:
                    pop_up_self (Button): This argument is the "self" call for the button we are binding the function to
                """
                self.league_env.play_pair_pt_2(winner, tie=tie)
                self.restart()
                self.league_env.play_pair(self.first_league_run)
                winner_popup.dismiss()

            content.bind(on_press=play_on)
        winner_popup.add_widget(content)
        winner_popup.open()

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
            self.league_env.play_pair_pt_1_5(result, AI_choice)

        # binding option_button button to each option
        for child in content.children:
            child.bind(on_press=option_button)
        # opening popup
        option_popup.open()

    def check_dot_pair(self, start, end):
        """Gives back the line index based on the pair of dots in kivy regardless of order from (dict) self.actual_lines

        Args:
            start (int): start dot index
            end (int): end dot index

        Returns:
            int: The index that cooresponds to a line in the BoardEnvironment's representation of the game board
        """
        try:
            return self.actual_lines[(start, end)]
        except KeyError:
            return self.actual_lines[(end, start)]

    def clear_game_screen(self):
        """Remove caputured box icons from screen"""
        # clear lines
        self.game_grid.canvas.remove_group("lines")

        # clear captured boxes
        for box in self.captured_boxes:
            box.parent.remove_widget(box)
        self.captured_boxes = []

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

        def play_again_button(inner_self):
            series_end_popup.dismiss()
            self.restart()
            self.clear_game_screen()
            self.league_env.play_pair(True)

        def end_game_button(inner_self):
            series_end_popup.dismiss()
            self.menu()

        content.children[1].bind(on_press=play_again_button)
        content.children[0].bind(on_press=end_game_button)
        series_end_popup.open()
