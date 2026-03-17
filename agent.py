from random import choice
from board import RawChessBoard, ChessBoardGUI
import copy
import math
import board

# TODO: Implement check avoidance in random move
# TODO: Optionally shuffle moves in get_moves_MCTS to avoid same moves playing out, import shuffle from random


# ----------------- NODE CLASS ---------------
class Node:
	""" Node class for MCTS tree
	"""
	def __init__(self, board:RawChessBoard, color, parent=None, move=None):
		self.board = board
		self.color = color
		self.parent = parent
		self.move = move

		self.children = []
		self.visits = 0
		self.wins = 0
		
		capture_moves, check_moves, other_moves = get_moves_MCTS(self.board, self.color)
		self.remaining_moves = capture_moves + check_moves + other_moves

	def is_fully_expanded(self):
		""" Checks if node is fully expanded (ie, all moves have been considered)
		"""
		return len(self.remaining_moves) == 0 # Node fully expanded iff no remaining moves left to expand
	

	def choose_best_child(self):
		""" Choose best child of node using UCB formula
		"""
		best_child = None
		best_ucb = float('-inf') # start wilath negative infinity; absolute minimum; any child node's UCB will be higher

		for child in self.children:
			ucb = get_UCB(child) # Calculate UCB for each child node
			if ucb > best_ucb:
				best_ucb = ucb		# update best UCB if new UCB score is better than current best
				best_child = child	# update best child so far (since this child would have best UCB)
		return best_child 			# selection complete -> returns best child to expand (type: None | Node)


# ----------------- MCTS AGENT CLASS - MAIN FUNCS ---------------
class MonteCarloChessAgent(object):
	""" MC agent is black player, moves semi-intelligently
	"""
	def __init__(self, color, opponent):
		self.color = color
		self.opponent = opponent


	def select(self, node:Node) -> Node :
		""" STAGE 1 of MCTS """
		while node.is_fully_expanded() and len(node.children) > 0: # Want current node to be expanded, but children to exist to select from
			node = node.choose_best_child() # Pick best child node to explore based on UCB score
		return node


	def expand(self, node:Node) -> Node :
		""" STAGE 2 of MCTS
		"""
		# Initialise key variables
		gameboard = node.board
		opp_color = 'white' if node.color == 'black' else 'black'
        
        # Pick untried move
		if len(node.remaining_moves) == 0:
			return node		# prevent crash if pop called on empty list
		next_move = node.remaining_moves.pop(0)
		src_row, src_col, dest_row, dest_col = next_move
		
        # Get next board state after necxt move
		next_state = gameboard.get_state_after_move(node.color, src_row, src_col, dest_row, dest_col)
		
        # copied board to avoid referencing issues
		child_gameboard = RawChessBoard(
            board=copy.deepcopy(next_state),
			number_of_total_moves=gameboard.number_of_total_moves+1,
			game_status=gameboard.game_status
        )
		
        # create new child node (expansion)
		child = Node(
            board=child_gameboard,
			color=opp_color,
			parent=node,
			move=next_move
        )
		
		node.children.append(child)
		return child                    # return expanded node for simulation


	def simulate(self, board_arg:RawChessBoard, color) -> int:
		""" STAGE 3 of MCTS
		"""
		simulation_board = copy.deepcopy(board_arg)
		current_player = color
		
		# Check for terminal conditions -- game over when checkmate
		for ply in range(board.MAX_NUM_PLY):
			if simulation_board.is_king_in_checkmate('white'):
				return 1
			elif simulation_board.is_king_in_checkmate('black'):
				return 0

			# Stratify move logic based on playout policy; varies black to white
			if current_player == "black":
				capture_moves, check_moves, other_moves = get_moves_MCTS(simulation_board, "black")
				if capture_moves:
					move = choice(capture_moves)
				elif check_moves:
					move = choice(check_moves)
				elif other_moves:
					move = choice(other_moves)
				else:
					return 0        # No moves means game over for black (checkmate)

			else:   # white (random) case
				move = random_move(simulation_board, "white")
				if move is None:
					return 1        # No moves for white = checkmate; ie black win

			# make change in simulated environment
			simulation_board.move_piece(current_player, move[0], move[1], move[2], move[3])
			current_player = 'white' if current_player == 'black' else 'black'          # swap colours for next ply
            
        # if max ply reached -> black loss
		return 0


	def backpropagate(self, node:Node, result):
		""" STAGE 4 of MCTS
		"""
		while node:
			node.visits += 1
			node.wins += result
			node = node.parent 		# Upwards traversal until root


	def get_next_move(self, gameboard:ChessBoardGUI): #must return src_row, src_col, dest_row, dest_col
		""" Skeleton putting togeter all four stages of MCTS
		"""
		root = Node(board=copy.deepcopy(gameboard.uboard), color=self.color)        # Deepcopy to avoid manipulating board when unintended
		
        # General skeleton for MCTS
		for _ in range(500):
			leaf:Node = self.select(root)
			child:Node = self.expand(leaf)
			result = self.simulate(child.board, child.color)
			self.backpropagate(child, result)

        # edge case -- root	w/ no children
		if len(root.children) == 0:
			return None
		
		best_child:Node = max(root.children, key=lambda c: c.visits)
		print("LINE 163: best_child move is", best_child.move, "with", best_child.visits, "visits and", best_child.wins, "wins")
		return best_child.move
		


# ----------------- RANDOM AGENT CLASS ---------------
class RandomChessAgent(object):
	""" RandomAgent player is the white player
	"""
	def __init__(self, color):
		self.color = color
		
	def get_next_move(self, gameboard:ChessBoardGUI, is_init=False): #must return src_row, src_col, dest_row, dest_col
		return random_move(gameboard.uboard, self.color) # Random move selection for random chess agent; also used for MCTS agent if no captures or check-giving moves are available



# ----------------- HELPER FUNCTIONS ---------------
def random_move(board:RawChessBoard, color):
	""" Function checks all possible moves, filters legal moves, and then picks a move at random
        Used for unintelligent random agent
	"""
	all_available_moves = board.get_playable_moves(color)	# Gets all playable moves at given state of the board for the agent's color
	
	valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
	if len(valid_moves) == 0:
		# raise Exception("No valid moves available for agent of color {0}".format(self.color))
		return None 	# No plays available
	
    # Random selection of moves
	selected_piece_moves = choice(valid_moves)		# Randomly selects a piece, as well as all its move choices
	
	# while True:
	selected_move = choice(selected_piece_moves["moves"])	# Randomly selects a move from the selected piece's move choices
	src_row, src_col, dest_row, dest_col = selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[1]
		# if not is_illegal_move(board, color, src_row, src_col, dest_row, dest_col):
			# break
	
	return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[1] # Move must be legal atp
	#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)


def get_UCB(node:Node, c=1.14):
	""" Function to calculate UCB score using UCB formula
	"""
	if node.visits == 0 or node.parent is None: # Unvisited & root node cases
		return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
	
	# UCB Formula
	exploit = node.wins / node.visits
	explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
	return exploit + explore


def get_moves_MCTS(board:RawChessBoard, color):
	""" Gets available, legal moves for MCTS
	"""
	# Captures > Check-giving moves > Random moves
	all_available_moves = board.get_playable_moves(color)

	# Initialisation of move arrays
	capture_moves = []
	check_moves = []
	remaining_moves = []
	opp_color = 'black' if color == 'white' else 'white' # gives_check takes opponent color

	# Converts moves from dict into target usable format
	for move in all_available_moves:
		src_row, src_col = move["row"], move["col"]

	# Evaluate possible moves from source coordinate
	# Check for captures, then check for check-giving moves -> Update arrays
		for dest_coordinates in move["moves"]:
			dest_row, dest_col = dest_coordinates

			# if not is_illegal_move(board, color, src_row, src_col, dest_row, dest_col):
				# If move is illegal, it is skipped -- not added to any of the move lists
			if board.is_capture(src_row, src_col, dest_row, dest_col):
				capture_moves.append((src_row, src_col, dest_row, dest_col)) # Filters capture moves
			elif board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
				check_moves.append((src_row, src_col, dest_row, dest_col))  # Filters check-giving moves
			else:
				remaining_moves.append((src_row, src_col, dest_row, dest_col)) # Remaining moves are stored for random gameplay in worst case of policy

	return capture_moves, check_moves, remaining_moves 


def is_illegal_move(board:RawChessBoard, color, src_row, src_col, dest_row, dest_col):
	""" Checks if this move would put the player in check, by looking a step ahead
	"""
	next_state = board.get_state_after_move(color, src_row, src_col, dest_row, dest_col)
	temp_board = RawChessBoard(
		board=copy.deepcopy(next_state),
		number_of_total_moves=board.number_of_total_moves,
		game_status=board.game_status
	)

	if temp_board.is_check(color):
		return True
	return False