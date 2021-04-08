import random as rand
from os import system
from collections import defaultdict

class BoardEnvironment:

    def __init__(self, kivy_obj):
        "init board"
        self.kivy_obj = kivy_obj

    def set_players(self, AI):
        self.AI = AI
        self.reset()

    def reset(self):
        self.turn = 'X'
        self.kivy_obj.piece = "X"

        self.board = list('---------')
        self.current_player = rand.random() < 0.5
        if not self.current_player:
            # if the current_player value is false, then its the AI turn
            choice = self.AI.select_action()
            self.board[choice] = self.turn
            self.kivy_obj.draw_turn(choice+1)
            self.turn = "O"
            self.kivy_obj.piece = "O"
        print("New Game")
        self.print_board()
        return self.current_player

    def print_board(self, board_string = None):
        B = self.board if not board_string else board_string
        check_for = ['X', 'O']
        print(B[0] if B[0] in check_for else 1,'|', B[1] if B[1] in check_for else 2,'|', B[2] if B[2] in check_for else 3, sep='')
        print('-----')
        print(B[3] if B[3] in check_for else 4,'|', B[4] if B[4] in check_for else 5,'|', B[5] if B[5] in check_for else 6, sep='')
        print('-----')
        print(B[6] if B[6] in check_for else 7,'|', B[7] if B[7] in check_for else 8,'|', B[8] if B[8] in check_for else 9, sep='')
        print()
        print('-----')
        

    def get_state(self):
        return "".join(self.board)

    def other_player(self):
        return not self.current_player

    def available_actions(self, first = None):
        return [ind for ind, val in enumerate(self.board) if val == '-']

    def play_game(self):
        self.reset()
        while( not self.is_full() ):
            system('clear')
            if( not self.current_player ):
                choice = self.AI.select_action(None)
            else:
                self.print_board()
                choices = self.available_actions(None)
                print("Select your space to play. Your pieces are", self.turn + '.', "Current choices are")
                print(list(x+1 for x in choices))
                choice = 10
                while(choice not in choices):
                    choice = input()
                    choice = int(choice) - 1
                    if(choice not in choices):
                        print("Spot not available. Current choices are")
                        print(list(x+1 for x in choices))

            self.board[choice] = self.turn

            if self.winner(self.turn):
                system('clear')
                if(self.current_player):
                    print("You won!")
                else:
                    print("You lost!")
                self.print_board()
                return self.current_player

            self.turn = 'X' if self.turn == 'O' else 'O'
            self.current_player = not self.current_player
        system('clear')
        self.print_board()
        print("Tie!")

        return None

    def play_game_turn(self, square_number):
        #user press button to assign X/O to board in board_env
        self.board[square_number - 1] = self.turn
        self.kivy_obj.draw_turn(square_number)
        
        if self.winner():
            # print winner message
            self.print_board()
            self.kivy_obj.winner()
            return
        self.turn = "X" if self.turn == "O" else "O"
        
        # let AI go
        if not self.is_full():
            choice = self.AI.select_action()
            self.kivy_obj.draw_turn(choice + 1)
            self.board[choice] = self.turn

            self.print_board()

            if self.winner():
                self.kivy_obj.winner()
                return
            if self.is_full():
                # There is a tie
                return
            self.turn = "X" if self.turn == "O" else "O"
            




    #returns true if there's a winner or false for no winner but not who is winner
    def winner(self):
        straight_lines = (
            (0,1,2),(3,4,5),(6,7,8),(0,3,6),
            (1,4,7),(2,5,8),(0,4,8),(2,4,6)
        )

        # if any of the straight lines on the board are set, return true
        return any(
            all(x == self.turn for x in (self.board[i] for i in line))
            for line in straight_lines
        )

    def is_full(self):
        return('-' not in self.board)