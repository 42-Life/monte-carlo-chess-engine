from random import choice
from board import RawChessBoard, ChessBoardGUI
import copy
import math

import board

class Node:
	# Node class for MCTS tree
	def __init__(self, board, parent=None, move=None):
		self.board = board
		self.parent = parent
		self.move = move
		self.children = []
		self.visits = 0
		self.wins = 0

class MonteCarloChessAgent(object):
	def __init__(self, color, opponent):
		self.color = color
		self.opponent = opponent

	# HELPERS FOR MCTS
	def get_UCB(node, c=1.41):
		if node.visits == 0:
			return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
		
		# UCB Formula
		exploit = node.wins / node.visits
		explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
		return exploit + explore
	

	# Defines the logic for playout policy: captures > check-giving; otherwise random. Used for single move at given state
	def playout_logic(self, board:RawChessBoard):
		# Initialisation of arrays
		capture_moves = []
		check_moves = []

		# Get legal (valid) moves at board state
		all_available_moves = board.uboard.get_playable_moves(self.color)
		valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
		if len(valid_moves) == 0:
			raise Exception("No valid moves available for agent of color {0}".format(self.color))
		
		# Check for captures, then check for check-giving moves -> Update arrays
		# Remove priority moves from random moves array
		for move in valid_moves:
			src_row, src_col = move["row"], move["col"]				# Get (source) row and col from move dict
			dest_row, dest_col = move["moves"][0], move["moves"][1] # Get destination coordinates from "moves" tuple in dict
			if board.uboard.is_capture_move(src_row, src_col, dest_row, dest_col):
				capture_moves.append((src_row, src_col, dest_row, dest_col)) # If move is capture move, add to capture moves array
			elif board.uboard.is_check_move(src_row, src_col, dest_row, dest_col):
				check_moves.append((src_row, src_col, dest_row, dest_col)) # If move is check move, add to check moves array

		# Evaluatate arrays, return move based on playout policy logic
		if len(capture_moves) > 0:
			return choice(capture_moves)
		elif len(check_moves) > 0:
			return choice(check_moves)
		else:
			return random_move(self, board)
			#NB: random_move will not return a capture or check-giving move, since these moves would have been checked for at this stage

	# MAIN STAGES MCTS
	def select(self, node):
	# STAGE 1: SELECTION (pick best node to explore based on UCB score)
		best_child = None
		best_ucb = float('-inf') # start with negative infinity; absolute minimum; any child node's UCB will be higher
		for child in node.children:
			ucb = self.get_UCB(child) # Gets UCB score for each child node
			if ucb > best_ucb:
				best_ucb = ucb		# update best UCB if new UCB score is better than current best
				best_child = child	# update best child so far (since this child would have best UCB)
		return best_child 			# selection complete -> returns best child to expand
		
	def expand(self, board):
		pass

	def simulate(self):
		pass

	def backpropagate(self):
		pass

	def get_next_move(self, board:RawChessBoard): #must return src_row, src_col, dest_row, dest_col
		#TODO: complete
		# Captures > Check-giving moves > Random moves
		# Enforce logic for higher value captures prioritised when multiple capture moves available? May not be necessary.
		return random_move(self, board)
		

class RandomChessAgent(object):
	def __init__(self, color):
		self.color = color

	def get_next_move(self, board:RawChessBoard, is_init=False): #must return src_row, src_col, dest_row, dest_col
		# raw_board = board.uboard # get instance of RawChessBoard to work with
		return random_move(self, board)
	

# HELPER FUNCTIONS
def random_move(self: MonteCarloChessAgent | RandomChessAgent, board:RawChessBoard):
		# Random Chess Agent acts randomly -- random piece selection, random move selection from that piece's available moveset
		# MCTS Agent does NOT act randomly, but needs random move selection if no captures or check-giving moves are available. Can use this function in that case.
		
		all_available_moves = board.uboard.get_playable_moves(self.color)	# Gets all playable moves at given state of the board for the agent's color

		# Account for cases where moves are not possible (avoid IndexError from choice() function)
		# Filters invalid moves
		valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
		if len(valid_moves) == 0:
			raise Exception("No valid moves available for agent of color {0}".format(self.color))

		# Random selection of moves
		selected_piece_moves = choice(valid_moves)		# Randomly selects a piece, as well as all its move choices
		selected_move = choice(selected_piece_moves["moves"])	# Randomly selects a move from the selected piece's move choices
		return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[-1]
		#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)