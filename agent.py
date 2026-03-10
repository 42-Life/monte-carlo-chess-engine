from random import choice
from board import RawChessBoard, ChessBoardGUI
import copy
import math

class MonteCarloChessAgent(object):
	def __init__(self, color, opponent):
		self.color = color
		self.opponent = opponent

	def get_UCB(self):
		#TODO: implement UCB formula for move selection
		return 0

	def get_next_move(self, board:RawChessBoard): #must return src_row, src_col, dest_row, dest_col
		#TODO: complete
		# Captures > Check-giving moves > Random moves
		# Enforce logic for higher value captures prioritised when multiple capture moves available? May not be necessary.
		return 0,0,0,0
		

class RandomChessAgent(object):
	def __init__(self, color):
		self.color = color

	def get_next_move(self, board:RawChessBoard, is_init=False): #must return src_row, src_col, dest_row, dest_col
		return random_move(self, board)
	

# HELPER FUNCTIONS
def random_move(self: MonteCarloChessAgent | RandomChessAgent, board:RawChessBoard):
		# Random Chess Agent acts randomly -- random piece selection, random move selection from that piece's available moveset
		# MCTS Agent does NOT act randomly, but needs random move selection if no captures or check-giving moves are available. Can use this function in that case.
		all_available_moves = RawChessBoard.get_playable_moves(board, self.color)	# Gets all playable moves at given state of the board for the agent's color
		selected_piece_moves = choice(all_available_moves)		# Randomly selects a piece, as well as all its move choices
		selected_move = choice(selected_piece_moves["moves"])	# Randomly selects a move from the selected piece's move choices
		return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[-1]
		#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)