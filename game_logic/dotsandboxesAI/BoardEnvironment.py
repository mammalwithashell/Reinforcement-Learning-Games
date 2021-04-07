import random
import copy

from . import Agent
# Import the agent object

"""
This file can be run as "python BoardEnvironment.py"

The Board environment keeps track of the board as the reinforcement algorithm understands it. 
"""

def select_difficulty():
    """Select the difficulty of the command line games

    Returns:
        None: 
    """
    x = 0
    diffdict = {1: r'game_logic\\dotsandboxesAI\\qtables\\easy.txt',
                2: r'game_logic\\dotsandboxesAI\\qtables\\medium.txt',
                3: r'game_logic\\dotsandboxesAI\\qtables\\hard.txt'}
    while(x > 3 or x < 1):
        print("Select a difficulty:")
        print("1: Easy")
        print("2: Medium")
        print("3: Hard")
        x = int(input())

    return diffdict[x]
class BoardEnvironment:
    """ this class creates an environment for agents to interact with"""

    def __init__(self, kivy_obj = None, agent:Agent = None):
        """
        Board environment for Agent to interact with and play
        This houses the command line version of the game
        
        board states are a 16-character representing the state of the board indices 0 - 11 are the lines and indices 12-15 are the score markers on the board 
        
        2x2 grid currently
        
        *-*-*
        |x|o|
        *-*-*
        |_|_|
        * * *
        
        
        choose which player goes first
        reset past action and past state of the Agent

        Args:
            kivy_obj (kivy.Screen, optional): The board needs the kivy screen to update the gui on certain game events. Leave blank for commandline run1. Defaults to None.
        """
        self.kivy_obj = kivy_obj
        self.agent = agent
        if self.agent:
            agent.environment = self
            self.reset()
        self.agent_turn = None
        

    def set_players(self, agent):
        " connects players with the environment "
        self.agent = agent
        self.reset()  # defines agent_turn
        self.score_board = {'X': 0, 'O': 0}
        if self.kivy_obj is not None:
            self.score_board = {"X": self.kivy_obj.score, "O": self.kivy_obj.ai_score}

    def reset(self):
        self.turn = 'X'  # the board always starts with X, regardless of which player

        """
        board states are a 16-character representing the state of the board indices 0 - 11 are the lines and indices 12-15 are the score markers on the board 
        
        2x2 grid currently
        
        *-*-*
        |x|o|
        *-*-*
        |_|_|
        * * *
        
        
        choose which player goes first
        reset past action and past state of the Agent
        """
        self.board = list('----------------')
        self.score_board = {'X': 0, 'O': 0}
        if self.kivy_obj is not None:
            self.score_board = {"X": self.kivy_obj.score, "O": self.kivy_obj.ai_score}
        self.agent.reset_past()
        if (random.random() < 0.5): 
            #randomly pick the player to start
            #if the ai starts and the kivy object is set
            self.agent_turn = True
            if self.kivy_obj is not None:
                self.play_game_turn()
            return True
        else:
            self.agent_turn = False
            return False

    def print_board(self, board_string=None):
        "print more readable board either from supplied board string or the current board"
        B = self.board if not board_string else board_string
        print('*',B[0],'*',B[1],'*')
        print(B[2],B[12],B[3],B[13],B[4])
        print('*',B[5],'*',B[6],'*')
        print(B[7],B[14],B[8],B[15],B[9])
        print('*',B[10],'*',B[11],'*')

    def get_state(self):
        return "".join(self.board)

    def other_player(self):
        # note, returns other player even if agent is playing itself
        return not self.agent_turn

    def available_actions(self):
        return [ind for ind, val in enumerate(self.board[:12]) if val == '-']

    def other_turn(self):
        return "X" if self.turn == "O" else "O"

    def play_game_turn(self, choice=None):
        # returns the winning player or None if a tie
        while True:
            if choice is None:
                # Let AI play
                # self.agent_turn = True
                ai = True
                if self.agent.past_state is None:
                    self.kivy_obj.piece = self.other_turn()
                choice = self.agent.select_action()


                self.kivy_obj.draw_ai_turn(choice, self.turn)
                print("Choice", choice)
            else:
                ai = False
                # self.print_board()
                print("SCOREBOARD", self.score_board)
                print("Your board piece is ", self.turn)
                print("Draw a line between two dots")
                print()
                self.kivy_obj.piece = self.turn



            # **********************************************
            # Update the board in memory (the list of Xs and Os)
            self.board[choice] = self.turn  # should check if valid

            score = self.winner(choice)

            # individual scores are stored in the scored_board dictionary with keys "X" and "O"
            # the length of the score list will be either 0, 1, 2
            self.score_board[self.turn] += len(score)
            if len(score) != 0:
                # if you score, don't swap players & go again
                # draw both center "X" or "O" characters
                for i in score:
                    self.board[i]=self.turn

                if not ai or self.is_full():
                    return True


                # the AI scored
                # update the ai score
                # set choice to none so ai will go again
                choice = None
                continue

            else:
                # switch players
                self.turn = self.other_turn()
                self.agent_turn = self.other_player()
                return False

        # TODO: update the score
    
    def user_choice(self, choice):
        # Update the board in memory (the list of Xs and Os)
        self.board[choice] = self.turn  # should check if valid
            
        score = self.winner(choice)
        
        # individual scores are stored in the scored_board dictionary with keys "X" and "O"
        # the length of the score list will be either 0, 1, 2
        self.score_board[self.turn] += len(score)
        if len(score) != 0:
            # if you score, don't swap players & go again
            # draw both center "X" or "O" characters
            for i in score:
                self.board[i]=self.turn

    def winner(self, choice):
        """Check for box completions and return the index for the box or boxes scored in the self.board object

        Args:
            choice (int): The index for the line choice in the self.board object

        Returns:
            list: List of scores, size 0 or 1
        """
        # map quads of lines to their box
        boxes = {
            (0, 2, 3, 5): 12, # top left box
            (1, 3, 4, 6): 13, # top right
            (5, 7, 8, 10): 14, # bottom left box
            (6, 8, 9, 11): 15 # bottom right box
        }
        score=[]
        for quad, box_index in boxes.items():
            if (choice in quad) and all(self.board[i] != '-' for i in quad):
                score.append(boxes[quad])
                if self.kivy_obj is not None:
                    self.kivy_obj.draw_captured_box(box_index, self.turn)
        if self.turn == self.kivy_obj.piece:
            self.kivy_obj.score += len(score)
        else:
            self.kivy_obj.ai_score += len(score)
        return score

    def is_full(self):
        """Check to see if the board is full

        Returns:
            bool: [description]
        """
        return ('-' not in self.board[0:12])

    def instructions(self):
        """Print instructions of commandline interface
        """
        print("Instructions:")
        print("To draw a line, enter the number of the corresponding line")
        print("*",str(0),"*",str(1),"*")
        print(str(2)," ",str(3)," ",str(4))
        print("*",str(5),"*",str(6),"*")
        print(str(7)," ",str(8)," ",str(9))
        print("*",str(10),"*",str(11),"*")
    
    def play_game(self):
        # returns the winning player or None if a tie
        self.reset()
        while True:
            # ************ HUMAN-PLAYABLE MODIFICATION
            if(self.agent_turn):
                choice = self.agent.select_action()
            else:
                print("SCOREBOARD", self.score_board)
                print("Your board piece is ", self.turn)
                print("Draw a line between two dots")
                self.print_board()
                movelist = self.available_actions()
                x = int(input())
                while(x not in movelist):
                    print("Invalid choice. Please select another board piece.")
                    x = int(input())
                print()
                choice = x

            self.board[choice] = self.turn  # should check if valid

            score = self.winner(choice)
            self.score_board[self.turn] += len(score)
            if len(score)!=0:
                # not a tie self.agent_turn.reward(100)
                for i in score:
                    self.board[i]=self.turn
                

            else:
                # switch players
                self.turn = self.other_turn()
                self.agent_turn = self.other_player()
                

            if self.is_full():
                break

        # Also added the scoreboard to display the final score
        if self.score_board[self.turn] > self.score_board[self.other_turn()]:
            print(self.turn, "won!")
            print("FINAL SCORE", self.score_board)
            self.print_board()
            return self.agent_turn
        elif self.score_board[self.turn] < self.score_board[self.other_turn()]:
            print(self.turn, "lost!")
            print("FINAL SCORE", self.score_board)
            self.print_board()
            return self.other_player()
        else:
            # it's a tie
            print("FINAL SCORE", self.score_board)
            self.print_board()
            return None
            
