from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Ellipse, Line, Color
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.uix.image import Image

import random as rand



# Import AI stuff
from .dotsandboxesAI.BoardEnvironment import BoardEnvironment
from .dotsandboxesAI.Agent import Agent
from .dotsandboxesAI.LeagueEnvironment import LeagueEnvironment

from time import sleep

"""
TODO

* Fix multiple turn error (player and ai should be able to go again if they score)
* Done Fix character change for ai after score

* Clean up UI & include scores for player and ai

* Fix order of turn calls making the ai choose on full board
* Draw "X" or "O" in box on score


* League Functionality by Wafi
"""

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

class DotsAndBoxesScreen(Screen):
    score = NumericProperty()
    ai_score = NumericProperty()
    game_grid = ObjectProperty(None)
    difficulty_setting = StringProperty("")
    match = StringProperty("")
    turn = BooleanProperty(True)
    piece = StringProperty("")
    lines = []
    
    # dictionary mapping box scores to their image widget
    captured_boxes = []
    
    
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
        8: [7, 5]
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
        (6, 7): 0
    }
    
    def restart(self):  
        """This function is run whenever the "Restart Game" Button is pressed
        """
        if self.lines:
            for line, start, end in self.lines:
                self.game_grid.canvas.remove(line)
        self.lines = []    
        self.board_env.reset()
        self.board_env.print_board()
        if self.captured_boxes != []:
            self.clear_captured_boxes() 
        
    def box_line(self, line_instruction):
        """Return points of line based on the instruction group names

        Args:
            line_instruction (kivy.instruction): Reference to the BoxLine object in the .kv file

        Returns:
            list: The points that the line needs to be drawn x1,y1,x2,y2
        """
        
        dots = {value:key for key, value in self.actual_lines.items()}
        return list(dots[line_instruction](0).pos) + list(dots[line_instruction](1).pos)
            
    def menu(self):
        """Swap screen back to title screen
        """
        if self.lines:
            for line, start, end in self.lines:
                self.game_grid.canvas.remove(line)
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        self.clear_captured_boxes()
    
    def clear_captured_boxes(self):
        """Remove caputured box icons from screen to
        """ 
        for box in self.captured_boxes:
            box.remove_from_cache()
    
    def load_settings(self, diff, match):
        """ 
        self.lines is a list of tuples containing
        a line instruction object
        the start dot number
        the end dot number
        """
        
        self.dots = [self.game_grid.canvas.get_group(f"dot{i}")[0] for i in range(9)]
        
        self.difficulty_setting = diff
        self.match = match
        
        # Load different settings based on game type
        if self.match == "Single Match":
            agent = Agent(f"game_logic/dotsandboxesAI/qtables/{self.difficulty_setting.lower()}.txt")
            self.board_env = BoardEnvironment(self, agent)
            self.board_env.reset()
            
            # self.board_env.set_players(agent)
            self.board_env.print_board()
        else:
            # League Match
            self.first_league_run = True
            league = LeagueEnvironment(self.board_env, self)

            player_names = []
            board_agents = []
            league_agents = []

            player_names.append('learning strategy and tactics')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'max'))

            player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/dotsandboxesAI/qtables/league.txt', 'random'))

            league.set_players(player_names, league_agents, board_agents)
            self.league_env = league
            self.scoreboard.size_hint_y = None
            self.scoreboard.height = 200
            for child in self.scoreboard.children:
                child.size_hint_y = None
                child.height = 200
    
    def on_touch_down(self, touch):
        # find what dot the mouse was over and save it to the start_dot property
        grace = int(self.dots[0].size[0] * 3)
        for i, dot in enumerate(self.dots):
            dotx, doty = [int(i) for i in dot.pos]
            # if touch is within a box twice the radius of the dot, we draw
            if int(touch.x) in range(dotx - grace, dotx + grace) and int(touch.y) in range(doty - grace, doty + grace):
                self.start_dot = i
                break
        return super().on_touch_down(touch)
    
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
    
    def on_touch_up(self, touch):
        # find what dot the mouse is over on mouse release and draw the appropriate line
        turn = self.board_env.turn
        for dot_index, dot_obj in enumerate(self.dots):
            # if touch is within a box twice the radius of the dot, we draw
            if self.check_for_dot_click(touch, dot_index, dot_obj):
                with self.game_grid.canvas:
                    # save line to lines property to be updated on_size
                    points = list(self.dots[self.start_dot].pos) + list(dot_obj.pos)
                    # add half dot radius to x and y for the line because the dot position is measured from bottom left corner of dots (the radius of the dot is 10)
                    points = [i + 15 for i in points]
                    Color(1, 0, 0)
                    self.lines.append((Line(points=points, width=3), self.start_dot, dot_index))
                
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
                    content = Label(text="AI is thinking...")
                    thinking_pop = Popup(content = content, size=(40, 60))
                    def think(instance):
                        # think for a spell
                        sleep(0.2)
                        instance.dismiss()
                    thinking_pop.bind(on_open=think)
                    thinking_pop.open()
                    
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
    
    def draw_ai_turn(self, choice):
        """Draw the line based on AI turn. This function is called with the board environment method play_game_turn

        Args:
            choice (int): Choice decided by the AI. 
        """
        
        # Reverse the dictionary of lines and dots and find the dots based on the ai choice
        dots = {value:key for key, value in self.actual_lines.items()}
        dots = dots[choice] # get the entry in the dictionary that maps the line indexes to the dot indexes
        
        with self.game_grid.canvas:
            # save line to lines property to be updated on_size
            points = list(self.dots[dots[0]].pos) + list(self.dots[dots[1]].pos)
            # add half dot radius to x and y for the line because the dot position is measured from bottom left corner of dots (the radius of the dot is 10)
            # The amount added to i should be half of the dot_size set in the dotsandboxes.kv file
            Color(0, 0, 1)
            points = [i + 15 for i in points]
            line = Line(points=points, width=3)
            self.lines.append((line, dots[0], dots[1]))
            
    def draw_captured_box(self, box_index, turn):
        
        # map box index to quadrant of grid
        boxes = {
            14:(0,1,3,4), # bottom left box
            15:(1,2,4,5), # bottom right box
            13:(4,5,8,7), # top right box
            12:(4,3,6,7) # top left box
        }
        
        avg_x, avg_y = 0, 0
        for dot_index in boxes[box_index]:
            print(self.dots[dot_index].pos[0], self.dots[dot_index].pos[1])
            avg_x += self.dots[dot_index].pos[0]
            avg_y += self.dots[dot_index].pos[1]
        avg_x /= 4
        avg_y /= 4
        print("Averages", avg_x, avg_y)
        
        color = "red" if turn == "X" else "blue"
        with self.canvas:
            image = Image(source=f"./images/dotsandboxes/{color}_{turn}.png", pos = (avg_x, avg_y))
        
            print("Pose",image.pos)
            self.captured_boxes.append(image)

        
    def is_full(self):
        """Display pop up when the board fills
        Called from within the self.board property of type BoardEnvironment

        Returns:
            None: Pop up that displays end condition of the game 
            win
            lose
            tie
        """
        
        
        winner_popup = Popup()
        # self.board.score_board is a dictionary of str:int with keys "X" and "O"
        other_piece = "X" if self.piece == "O" else "O"
        if self.board_env.score_board[self.piece] > self.board_env.score_board[other_piece]:
            content = Button(text=f"You are the winner")
        elif self.board_env.score_board[self.piece] < self.board_env.score_board[other_piece]:
            content = Button(text=f"Computer is the winner")
        else:# it's a tie
            content = Button(text=f"There was a tie!")
        self.board_env.print_board()
        content.bind(on_press=winner_popup.dismiss)
        winner_popup.add_widget(content)
        winner_popup.open()
    
    def check_for_dot_click(self, touch, dot_index, dot_obj):
        """Check if the user clicked a second dot valid with the current dot

        Args:
            touch (Touch): Kivy touch object
            dot_index (int): Index of dot we are checking
            dot_obj (kivy.Instruction): The object in memory that represents the dot drawing

        Returns:
            bool: Returns true if the dot that the user lets go of the mouse over is a valid pair with the dot from click
        """        
        
        grace_ratio = 1
        grace = int(self.dots[0].size[0] * grace_ratio)
        dotx, doty = [int(i) for i in dot_obj.pos]
        
        # warning monster bool
        return (int(touch.x) in range(dotx - grace, dotx + grace) and int(touch.y) in range(doty - grace, doty + grace) and self.start_dot is not None and dot_index in self.accepted_lines[self.start_dot] and self.check_dot_pair(dot_index, self.start_dot) in self.board_env.available_actions())

    """def on_size(self, instance, value):
        for line, start, end in self.lines:
            self.game_grid.canvas.remove(line)"""
    
