import random as random
import copy
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

	#return board state
	def get_state(self):
		return "".join(self.board)

	#return the lowest board piece available for the selected column
	def get_lowest_column(self, i):
		if (self.board[i] == '-'):
			while i < 20:
				if(self.board[i+5] == '-'):
					i = i + 5
				else:
					break
		else:
			return -1
		return i

	#select the chosen piece at the board level and flip the turn
	def select_piece(self, choice, turn):
		self.board[choice] = turn
		self.turn = 'X' if (turn == 'O') else 'O'

	def other_player(self):
		# note, returns other player even if playerA is playing itself
		return not self.current_player

	#return all of the columns available for selection
	def available_actions(self, change_buttons=False):
		movelist = []
		buttons = {
			0: self.kivy_obj.button_one,
			1: self.kivy_obj.button_two,
			2: self.kivy_obj.button_three,
			3: self.kivy_obj.button_four,
			4: self.kivy_obj.button_five
		}
		for i in range(5):
			if self.board[i] == '-':
				movelist.append(i)
				if change_buttons:
					buttons[i].visible = True
					buttons[i].disabled = False
			else:
				if change_buttons:
					buttons[i].visible = False
					buttons[i].disabled = True
				continue
		return movelist

	#determine if there is a winner based on the pre-calculated win states
	def winner(self, check_for = ['X', 'O']):
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
		(9,14,19,24))
		for turn in check_for:
			for line in straight_lines:
				if all(x == turn for x in (self.board[i] for i in line)):
					return turn
		return '' # if there is no winner
	#determine if board is full
	def is_full(self):
		return('-' not in self.board)