from random import choice
from board import RawChessBoard, ChessBoardGUI
import copy
import math

import board

class Node:
	# Node class for MCTS tree
	def __init__(self, board:RawChessBoard, color, parent=None, move=None):
		self.board = board
		self.color = color
		self.parent = parent
		self.move = move

		self.children = []
		self.visits = 0
		self.wins = 0
		# self.remaining_moves = playout_policy(board) # List of all moves that can be made from this node's board state; used for expansion
		self.remaining_moves = self.get_all_moves() # List of all moves that can be made from this node's board state; used for expansion


	def get_all_moves(self):
		# Captures > Check-giving moves > Random moves
		all_available_moves = self.board.get_playable_moves(self.color)

		# Initialisation of move arrays
		capture_moves = []
		check_moves = []
		remaining_moves = []
		opp_color = 'black' if self.color == 'white' else 'white' # gives_check takes opponent color

		# Converts moves from dict into target usable format
		for move in all_available_moves:
			src_row, src_col = move["row"], move["col"]

		# Evaluate possible moves from source coordinate
		# Check for captures, then check for check-giving moves -> Update arrays
			for dest_coordinates in move["moves"]:
				dest_row, dest_col = dest_coordinates
				if self.board.is_capture(src_row, src_col, dest_row, dest_col):
					capture_moves.append((src_row, src_col, dest_row, dest_col)) # Filters capture moves
				elif self.board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
					check_moves.append((src_row, src_col, dest_row, dest_col))  # Filters check-giving moves
				else:
					remaining_moves.append((src_row, src_col, dest_row, dest_col)) # Remaining moves are stored for random gameplay in worst case of policy

		return capture_moves + check_moves + remaining_moves 
		# Moves are listed in priority order
	

	def is_fully_expanded(self):
		return len(self.remaining_moves) == 0 # Node fully expanded iff no remaining moves left to expand
	
	
	def choose_best_child(self):
		best_child = None
		best_ucb = float('-inf') # start with negative infinity; absolute minimum; any child node's UCB will be higher

		for child in self.children:
			ucb = get_UCB(child) # Calculate UCB for each child node
			if ucb > best_ucb:
				best_ucb = ucb		# update best UCB if new UCB score is better than current best
				best_child = child	# update best child so far (since this child would have best UCB)
		return best_child 			# selection complete -> returns best child to expand (type: None | Node)



class MonteCarloChessAgent(object):
	def __init__(self, color, opponent):
		self.color = color
		self.opponent = opponent
		

	# MAIN STAGES MCTS
	def select(self, node:Node):
		# STAGE 1: SELECTION (pick best node to explore based on UCB score)
		while node.is_fully_expanded() and len(node.children) > 0: # Want current node to be expanded, but children to exist to select from
			node = node.choose_best_child() # Pick best child node to explore based on UCB score
		return node
			
		
	def expand(self, node:Node):
		board = node.board # Board state of current node
		# STAGE 2: EXPANSION (expand node by adding child node corresponding to move selected from remaining moves)
		if not node.remaining_moves:
			return node # If true, no moves to expand and current node is a leaf/terminal node. Can simply return this node.
		
		# Pick next move to expand from movelist (in priority order)
		next_move = node.remaining_moves.pop(0) # Get next move to expand; remove mv from movelist
		
		# capture_moves, check_moves, remaining_moves = node.remaining_moves
		# if capture_moves:
		# 	next_move = capture_moves.pop(0) # Get next move to expand; remove mv from movelist
		# elif check_moves:
		# 	next_move = check_moves.pop(0) # Get next move to expand; remove mv from movelist
		# else:
		# 	next_move = choice(remaining_moves) # Random selection from non-priority movelist
		# 	remaining_moves.remove(next_move) # Remove mv from movelist

		src_row, src_col, dest_row, dest_col = next_move
		
		# Next state -- Type: 2D list
		new_board_state = board.get_state_after_move(src_row, src_col, dest_row, dest_col) # Get new board state after making this move; will be used as board state for child node

		# Expand new child
		child_board = RawChessBoard(
			board=copy.deepcopy(new_board_state),
			number_of_total_moves=board.number_of_total_moves + 1,	# increment steps made in deepcopy version of game
			game_status=board.game_status
		)

		child = Node(
			board=child_board,
			color='black' if node.color == 'white' else 'white', # Child node = opposing color
			parent=node,
			move=next_move
		)

		node.children.append(child) # Add this new child to the list of children of the current node
		return child # Return child node (just expanded)


	def simulate(board_arg:RawChessBoard, color):
		pass
		# To be implemented
		# game_state = board_arg
		# current = color

		# for ply in range(board.MAX_NUM_PLY):		# Imposts max ply constant from board.py. This 'board' NOT to be confused with board attribute
		# 	playable_moves = game_state.get_playable_moves(current) # Get playable moves for current color at this game state
		# 	if len(playable_moves) == 0: # Game over
		# 		break

		# 	valid_moves = get_valid_moves(playable_moves) # valid moves -- formatted as (sr,sc,dr,dc)
		# 	if current == "white":
		# 		move = choice(valid_moves)
		# 	else:
		# 		pass

		# 	pass

		

	def backpropagate(self):
		# To be implemented
		pass

	def get_next_move(self, gameboard:RawChessBoard): #must return src_row, src_col, dest_row, dest_col
		root = Node(gameboard, color=self.color) # Create root node for MCTS tree with current board state and agent's color
		for _ in range(100):
			leaf = self.select(root)
			child = self.expand(leaf, gameboard)
			result = self.simulate(child.board, child.color)
			self.backpropagate(child, result)
		
		best_child = max(root.children, key=lambda c: c.visits) # Picks child with most visits -- ie best child
		return best_child.move # Return move corresponding to best child
		

class RandomChessAgent(object):
	def __init__(self, color):
		self.color = color

	# Main logic for MCTS agent
	def get_next_move(self, board:RawChessBoard, is_init=False): #must return src_row, src_col, dest_row, dest_col
		return random_move(self, board) # Random move selection for random chess agent; also used for MCTS agent if no captures or check-giving moves are available
	

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
	return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[1]
	#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)

def get_UCB(node:Node, c=1.41):
	if node.visits == 0 | node.parent is None: # Unvisited & root node cases
		return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
	
	# UCB Formula
	exploit = node.wins / node.visits
	explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
	return exploit + explore



# --------------------------------- CODE GRAVEYARD ---------------------------------

# Within MonteCarloChessAgent class:

	#TODO: Double check MCTS main implementation
	#TODO: Check whether functions should be methods under Node or under MonteCarloChessAgent

	# HELPERS FOR MCTS
	# def get_UCB(node, c=1.41):
	# 	if node.visits == 0:
	# 		return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
		
	# 	# UCB Formula
	# 	exploit = node.wins / node.visits
	# 	explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
	# 	return exploit + explore
	
	# def pick_best_child(node):
	# 	for child in node.children:
	# 		child.ucb = get_UCB(child) # Calculate UCB for each child node
	# 	pass

	# # Gets all valid moves for agent using get_playable_moves, puts them in form (src_row, src_col, dest_row, dest_col)
	# def get_valid_moves(self, board):
	# 	all_available_moves = board.uboard.get_playable_moves(self.color)
	# 	all_valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
	# 	valid_moves = []

	# 	# Converts moves from dict to target usable format
	# 	for move in all_valid_moves:
	# 		src_row, src_col = move["row"], move["col"]				# Get (source) row and col from move dict
	# 		dest_row, dest_col = move["moves"][0], move["moves"][1] # Get destination coordinates from "moves" tuple in dict
	# 		valid_moves.append(src_row, src_col, dest_row, dest_col)
	# 	return valid_moves

# GET_VALID_MOVES
# def get_valid_moves(self:MonteCarloChessAgent | Node, board:RawChessBoard):
	# all_available_moves = board.get_playable_moves(self.color)
	# all_valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
	# valid_moves = []

	# # Converts moves from dict to target usable format
	# for move in all_valid_moves:
	# 	src_row, src_col = move["row"], move["col"]				# Get (source) row and col from move dict

	# 	# Evaluate possible moves from source coordinates:
	# 	for dest_coordinates in move["moves"]:
	# 		valid_moves.append((src_row, src_col, dest_coordinates[0], dest_coordinates[1]))

	# return valid_moves
	# pass

	# # LOGIC STRUCTURE: Picks best move at given state based on playout logic
	# def playout_policy(self, board:RawChessBoard):
	# 	# Captures > Check-giving moves > Random moves
	# 	# Initialisation of move arrays
	# 	capture_moves = []
	# 	check_moves = []
	# 	opp_color = 'black' if self.color == 'white' else 'white'

	# 	# Get valid moves for agent at current board state; returns list of moves in form (src_row, src_col, dest_row, dest_col)
	# 	valid_moves = get_valid_moves(self, board)
		
	# 	# Check for captures, then check for check-giving moves -> Update arrays
	# 	# Remove priority moves from random moves array
	# 	for move in valid_moves:
	# 		src_row, src_col, dest_row, dest_col = move[0], move[1], move[2], move[3]
	# 		if board.is_capture(src_row, src_col, dest_row, dest_col):
	# 			capture_moves.append((src_row, src_col, dest_row, dest_col)) # If move is capture move, add to capture moves array
	# 		elif board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
	# 			check_moves.append((src_row, src_col, dest_row, dest_col)) # If move is check move, add to check moves array

	# 	# Evaluatate arrays, return move based on playout policy logic
	# 	if len(capture_moves) > 0:
	# 		return choice(capture_moves)
	# 	elif len(check_moves) > 0:
	# 		return choice(check_moves)
	# 	else:
	# 		return random_move(self, board)
	# 		#NB: random_move will not return a capture or check-giving move, since these moves would have been checked for at this stage