from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Ellipse, Line
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window

# Import AI stuff
from .dotsandboxesAI.boardenvironment import BoardEnvironment
from .dotsandboxesAI.agent import Agent
from .dotsandboxesAI.leagueenvironment import LeagueEnvironment



"""
TODO

* Include AI
* Clean up UI
* League Functionality
"""

class DotsAndBoxesScreen(Screen):
    score = NumericProperty()
    ai_score = NumericProperty()
    game_grid = ObjectProperty(None)
    difficulty_setting = StringProperty("")
    match = StringProperty("")
    turn = BooleanProperty(True)
    
    
    def setup(self):    
        for line, start, end in self.lines:
            self.game_grid.canvas.remove(line)
        self.lines = []
            
    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "title"
        
    def load_settings(self, diff, match):
        """ 
        self.lines is a list of tuples containing
        a line instruction object
        the start dot number
        the end dot number
        """
        self.lines = []
        
        # a dictionary mapping dot numbers to acceptable dots to be paired with
        self.accepted_lines = {
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
        self.actual_lines = {
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
        self.dots = [self.game_grid.canvas.get_group(f"dot{i}")[0] for i in range(9)]
        self.difficulty_setting = diff
        self.match = match
        
        # Load different settings based on game type
        if self.match == "Single Match":
            pass
        else:
            # League Match
            pass
    
    def on_touch_down(self, touch):
        # find what dot the mouse was over and save it to the start_dot property
        grace = int(self.dots[0].size[0] * 2)
        for i, dot in enumerate(self.dots):
            dotx, doty = [int(i) for i in dot.pos]
            # if touch is within a box twice the radius of the dot, we draw
            if int(touch.x) in range(dotx - grace, dotx + grace) and int(touch.y) in range(doty - grace, doty + grace):
                self.start_dot = i
                break
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # find what dot the mouse is over on mouse release and draw the appropriate line
        grace = int(self.dots[0].size[0] * 2)
        for i, dot in enumerate(self.dots):
            dotx, doty = [int(i) for i in dot.pos]
            # if touch is within a box twice the radius of the dot, we draw
            if int(touch.x) in range(dotx - grace, dotx + grace) and int(touch.y) in range(doty - grace, doty + grace) and i in self.accepted_lines[self.start_dot]:
                with self.game_grid.canvas:
                    # save line to lines property to be updated on_size
                    points = list(self.dots[self.start_dot].pos) + list(dot.pos)
                    # add half dot radius to x and y for the line because the dot position is measured from bottom right of dots me
                    points = [i + 5 for i in points]
                    line = Line(points=points)
                    self.lines.append((line, self.start_dot, i))
                    
                    # try except pairs to return line choice
                    try:
                        self.actual_lines[(self.start_dot, i)]
                    except KeyError:
                        self.actual_lines[(i, self.start_dot)]
                        
        return super().on_touch_up(touch)
    
    def play_game(self):
        pass
    
    """def on_size(self, instance, value):
        for line, start, end in self.lines:
            self.game_grid.canvas.remove(line)"""
    
