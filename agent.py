# from random import choice
# from board import RawChessBoard, ChessBoardGUI
# import copy
# import math

# import board

# # ---------------------------------------- CHANGELOG: BUG FIXES -------------------------------

# #TODO: Optimise/abide by chess rules: White does not move king when in check. Chess rules dictate that a player in check MUST move out of check, so long as a move exists to exit check (ie: not a checkmate case)
# #BUG: Fix (observations)
# 	# Pawns don't capture when they are able to -- Black MCTS
# 	# MCTS agent sometimes throws "NO Valid moves available" error, even when moves are available (pawn moves: including non-capture movement)
# 	# Pieces change positions / appear/disappear randomly sometimes -> observed happenign during check on white king
# 	# TWICE: Board resets semi-randomly after white king in check
# 	# Gets stuck in local max sometimes (eg: white rook moves back and forth between two squares, since no captures or check-giving moves available for white
# 		# MCTS exploration/exploitation balance issue? -- how to fix without changing c?
# 		# Perhaps add some randomness to move selection for MCTS agent when multiple moves have same UCB score? (eg: random selection among best children, rather than always picking first best child)
# 		# In case of rook, it moves between two squares, each with 3 visits and 0 wins
# """
# 	LINE 188: best_child move is (0, 1, 0, 0) with 3 visits and 0 wins
# 	Move 92 made
# 	Move 93 made
# 	LINE 188: best_child move is (0, 0, 0, 1) with 3 visits and 0 wins
# 	Move 94 made
# 	Move 95 made

# 	This cycle repeats
# """			

# #TODO FIX: Need to split capture moves, check-giving moves, remaining moves into three DIFFERENT lists and then randomly select conditionally
# # ie if priority_1 moves is non-empty list, then randomly select from there.
# # do not just pop(0) -- this is leading to the rook repitition

# # Splitting moves into 3 diff lists and processing them hierarchally DOES introduce smoother randomisation
# # HOWEVER, random board reset BUG when white king is in check remains a major problem
# 	# In one game, the white king disappears, but gameplay continues

# # TODO Fix: evade check -- method within random that filters all actions available, only considering check-evading moves
# # If one cannot be played, then terminal state is reached and opponent wins

# """ Mar 17: 
# 	Still randomises move after white check, even with evade_check implemented
# 	Analysis -- seems to play 3 moves when in check? But sometimes king disappears

# 	OBSERVATION
# 	* Moves being made with 1 visit & 0 wins (used to have more visits and wins -- what edit changed this?)

# 	EXPAND functionality
# 	* Introduce castling as a possible move(?)

# 	BUG -- illegal moves
# 	* White is able to move into check (illegal move)
# 	* White king captured its own piece in one case

# 	BUG -- funcionality gaps
# 	* Pawns can be check-giving pieces (game does not recognise pawn as check-giving threats -- both for MCTS move choice & randomAgent check-evasion)

# 	PROBLEM -- choose_best_child and get_ucb are just not being run. UCB formula is not being used for game logic
# 		Selection stage does not return UCB. Node DOES have visits, but does not have any wins counted towards it
# 		# visits increment with each successive node in the select stage?
# """

# # UNTESTED FIXES: 
# # node.color instead of self.color in expand() smartestmove call 
# # Fixed indentation in convert moves format + removed isRandom argument
# # Adjusted expand() func to old implementation --> TODO double check if priority tri-list adaption is needed (eg: to avoid rook repetition)
# # Changed check_evade so that temp_board is deepcopied and we see if move is_check in that one-step simulation
# # Alt implementation of best_child in get_next_move
# # deepcopy tempboard implementation in get_moves_MCTS


# class Node:
# 	# Node class for MCTS tree
# 	def __init__(self, board:RawChessBoard, color, parent=None, move=None):
# 		self.board = board
# 		self.color = color
# 		self.parent = parent
# 		self.move = move

# 		self.children = []
# 		self.visits = 0
# 		self.wins = 0

# 		# self.capture_moves, self.check_moves, self.other_moves = self.get_all_moves()	# Get all moves produces 3 lists
# 		# self.remaining_moves = self.capture_moves + self.check_moves + self.other_moves # List of all moves that can be made from this node's board state; used for expansion
# 		capture_moves, check_moves, other_moves = self.get_all_moves()
# 		self.remaining_moves = capture_moves + check_moves + other_moves


# 	def get_all_moves(self):
# 		# Captures > Check-giving moves > Random moves
# 		return get_moves_MCTS(self.board, self.color)
	

# 	def is_fully_expanded(self):
# 		return len(self.remaining_moves) == 0 # Node fully expanded iff no remaining moves left to expand
	
	
# 	def choose_best_child(self):
# 		best_child = None
# 		best_ucb = float('-inf') # start with negative infinity; absolute minimum; any child node's UCB will be higher

# 		for child in self.children:
# 			ucb = get_UCB(child) # Calculate UCB for each child node
# 			if ucb > best_ucb:
# 				best_ucb = ucb		# update best UCB if new UCB score is better than current best
# 				best_child = child	# update best child so far (since this child would have best UCB)
# 		print("LINE 95: best UCB=", best_ucb)
# 		return best_child 			# selection complete -> returns best child to expand (type: None | Node)



# class MonteCarloChessAgent(object):
# 	def __init__(self, color, opponent):
# 		self.color = color
# 		self.opponent = opponent
		

# 	# MAIN STAGES MCTS
# 	def select(self, node:Node) -> Node :
# 		# STAGE 1: SELECTION (pick best node to explore based on UCB score)
# 		while node.is_fully_expanded() and len(node.children) > 0: # Want current node to be expanded, but children to exist to select from
# 			node = node.choose_best_child() # Pick best child node to explore based on UCB score
# 			print("LINE 111: choose_best_child_was run")
		
# 		print("Selected node:", node.color, node.visits, node.wins)
# 		return node
			
		
# 	def expand(self, node:Node) -> Node :
# 		board = node.board # Board state of current node
# 		# STAGE 2: EXPANSION (expand node by adding child node corresponding to move selected from remaining moves)

# 		# ALT APPROACh
# 		# Pick next move to expand from movelist (in priority order)
# 		# next_move = smartest_move_MCTS(node.board, node.color)
# 		# if next_move == None:
# 			# return node		# If true, no moves to expand and current node is a leaf/terminal node. Can simply return this node.

# 		# if max(len(node.capture_moves), len(node.check_moves), len(node.other_moves)) == 0:
# 		if len(node.remaining_moves) == 0:
# 			return node		# If true, no moves to expand and current node is a leaf/terminal node. Can simply return this node.
		
# 		next_move = node.remaining_moves.pop(0)		# Removes top move from prioritised remaining moves list

# 		# next_move = node.remaining_moves.pop(0) # Get next move to expand; remove mv from movelist
# 		src_row, src_col, dest_row, dest_col = next_move
		
# 		# Next state -- Type: 2D list
# 		new_board_state = board.get_state_after_move(node.color, src_row, src_col, dest_row, dest_col) # Get new board state after making this move; will be used as board state for child node

# 		# Expand new child
# 		child_board = RawChessBoard(
# 			board=copy.deepcopy(new_board_state),
# 			number_of_total_moves=board.number_of_total_moves + 1,	# increment steps made in deepcopy version of game
# 			game_status=board.game_status
# 		)

# 		child = Node(
# 			board=child_board,
# 			color='black' if node.color == 'white' else 'white', # Child node = opposing color
# 			parent=node,
# 			move=next_move
# 		)

# 		node.children.append(child) # Add this new child to the list of children of the current node
# 		return child # Return child node (just expanded)


# 	def simulate(self, board_arg:RawChessBoard, color) -> int:
# 		# STAGE 3: SIMULATION (play out game from this child node using playout policy; return result of playout)

# 		# Copy of board so original board is not modified during simulation
# 		# Uses deepcopy on the underlying board
# 		simulation_board = copy.deepcopy(board_arg)

# 		current_player = color

# 		for ply in range(board.MAX_NUM_PLY):

# 			# Break is game is already done
# 			if simulation_board.is_terminal(current_player) or simulation_board.is_king_in_checkmate(current_player):
# 				break
			
# 			if current_player == "white":
# 				# White player: Random (unintelligent) play
# 				move = random_move(self, simulation_board, current_player) # Random move selection for white player. Explicitly passes white as colour, since self (MCTS agent) is black

# 			else:
# 				# Black player: Playout policy (intelligent)
# 				move = smartest_move_MCTS(simulation_board, current_player)

# 			# Break if no moves available for current player (ie checkmate/stalemate)
# 			if move is None: 	# None logic implemented in random_move (for white) and smartest_move_MCTS (for black)
# 				break

# 			# Simulate gameplay
# 			simulation_board.move_piece(current_player, move[0], move[1], move[2], move[3]) # Update state of board to reflect simulated move (ie make the move on the board)
# 			# print("LINE 152: Simulation move made: player was", current_player, ". move was", move)

# 			# Players change turns
# 			current_player = 'black' if current_player == 'white' else 'white'

# 		# Eval function @ end of (simulated) game
# 		if simulation_board.is_king_in_checkmate(self.opponent): # If opponent is in checkmate, this is a win for the MCTS agent
# 			return 1
# 		elif simulation_board.is_king_in_checkmate(self.color): # If MCTS agent is in checkmate, this is a loss for the MCTS agent
# 			return 0
# 		else:
# 			return 0 	# Should only occur if max ply is exceeded before checkmate
# 		# TODO: Adjust reward function: win:-1, draw:0


# 	def backpropagate(self, node:Node, result:int):
# 		# STAGE 4: BACKPROPAGATION (update win/visit counts along path from child to root based on result of simulation playout)
# 		while node is not None:		# Terminates after root case (root.parent = None)
# 			node.visits += 1
# 			# print("LINE 197: Node", node, "was visited. # visits =", node.visits)
# 			node.wins += result
# 			# print("LINE 199: Node", node, "increased score by", result, ". Total wins =", node.wins)
# 			node = node.parent 		# Upwards traversal until root


# 	def get_next_move(self, gameboard:ChessBoardGUI): #must return src_row, src_col, dest_row, dest_col
# 		root = Node(copy.deepcopy(gameboard.uboard), color=self.color) # Create root node for MCTS tree with current board state and agent's color
# 		# Deepcopy to avoid manipulating actual game board during MCTS; once next_move is returned, THEN real gameboard updated in main.py
# 		for _ in range(100):
# 			leaf:Node = self.select(root)
# 			child:Node = self.expand(leaf)
# 			result = self.simulate(child.board, child.color)
# 			self.backpropagate(child, result)
		
# 		# Alt implementation best_child
# 		# best_child:Node = None
# 		# best_score = float('-inf')
# 		# for child in root.children:
# 		# 	if child.visits == 0:
# 		# 		score = -1
# 		# 	else:
# 		# 		score = child.wins / child.visits

# 		# 	if score > best_score:
# 		# 		best_score = score
# 		# 		best_child = child

# 		best_child:Node = max(root.children, key=lambda c: c.visits) # Picks child with most visits -- ie best child

# 		print("LINE 188: best_child move is", best_child.move, "with", best_child.visits, "visits and", best_child.wins, "wins")
# 		return best_child.move # Return move corresponding to best child
# 		# return random_move(self, gameboard.uboard, self.color) # TESTING ONLY. COMMENT ABOVE, COMMENT HERE AS NEEDED

# class RandomChessAgent(object):
# 	def __init__(self, color):
# 		self.color = color


# 	def evade_check(self, gameboard:RawChessBoard):
# 		""" To abide by the rules of chess, the white agent pauses entirely random movement and forces a move that evades check
# 		 	If this is impossible, then checkmate and game is done. Written partly to deal with bug where game board 'resets' semirandomly when white is in check
# 			Only called once board is in check
# 		"""
# 		check_evasion_moves = []

# 		all_moves = gameboard.get_playable_moves(self.color)
# 		usable_moves = convert_moves_format(all_moves)

# 		# Find valid check evasion moves
# 		for move in usable_moves:
# 			next_state = gameboard.get_state_after_move(self.color, move[0], move[1], move[2], move[3])

# 			temp_board = RawChessBoard(
# 				board=copy.deepcopy(next_state),
# 				number_of_total_moves=gameboard.number_of_total_moves,
# 				game_status=gameboard.game_status
# 			)

# 			if not temp_board.is_check(self.color):
# 				check_evasion_moves.append(move)

# 		#TODO: If empty with no move, checkmate ie terminal state
# 		if len(check_evasion_moves) == 0:
# 			return None			# checkmate state
# 		else:
# 			return choice(check_evasion_moves)		# random selection from valid moveset


# 	# Main logic for MCTS agent
# 	def get_next_move(self, gameboard:ChessBoardGUI, is_init=False): #must return src_row, src_col, dest_row, dest_col

# 		underlying_board:RawChessBoard = gameboard.uboard
# 		if underlying_board.is_check(self.color):
# 			move = self.evade_check(underlying_board)
# 			if move == None or underlying_board.is_king_in_checkmate(self.color):
# 				print("LINE 270: No move available for  white")
# 				return None

# 		return random_move(self, gameboard.uboard, self.color) # Random move selection for random chess agent; also used for MCTS agent if no captures or check-giving moves are available
	

# # HELPER FUNCTIONS
# def random_move(agent: MonteCarloChessAgent | RandomChessAgent, board:RawChessBoard, color):
# 	# Random Chess Agent acts randomly -- random piece selection, random move selection from that piece's available moveset
# 	# MCTS Agent does NOT act randomly, but needs random move selection if no captures or check-giving moves are available. Can use this function in that case.
	
# 	all_available_moves = board.get_playable_moves(color)	# Gets all playable moves at given state of the board for the agent's color

# 	# Account for cases where moves are not possible (avoid IndexError from choice() function)
# 	# Filters invalid moves
# 	valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
# 	if len(valid_moves) == 0:
# 		return None 	# No plays available

# 	# Random selection of moves
# 	selected_piece_moves = choice(valid_moves)		# Randomly selects a piece, as well as all its move choices
# 	selected_move = choice(selected_piece_moves["moves"])	# Randomly selects a move from the selected piece's move choices
# 	return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[1]
# 	#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)


# def get_UCB(node:Node, c=1.41):
# 	if node.visits == 0 or node.parent is None: # Unvisited & root node cases
# 		return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
	
# 	# UCB Formula
# 	exploit = node.wins / node.visits
# 	explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
# 	return exploit + explore


# def get_moves_MCTS(board:RawChessBoard, color):
# 	# Captures > Check-giving moves > Random moves
# 	all_available_moves = board.get_playable_moves(color)

# 	# Initialisation of move arrays
# 	capture_moves = []
# 	check_moves = []
# 	remaining_moves = []
# 	opp_color = 'black' if color == 'white' else 'white' # gives_check takes opponent color

# 	# Converts moves from dict into target usable format
# 	for move in all_available_moves:
# 		src_row, src_col = move["row"], move["col"]

# 	# Evaluate possible moves from source coordinate
# 	# Check for captures, then check for check-giving moves -> Update arrays
# 		for dest_coordinates in move["moves"]:
# 			dest_row, dest_col = dest_coordinates

# 			next_state = board.get_state_after_move(color, src_row, src_col, dest_row, dest_col)

# 			temp_board = RawChessBoard(
# 				board=copy.deepcopy(next_state),
# 				number_of_total_moves=board.number_of_total_moves,
# 				game_status=board.game_status
# 			)

# 			if board.is_capture(src_row, src_col, dest_row, dest_col):			# Original board since capture happened apread
# 				capture_moves.append((src_row, src_col, dest_row, dest_col))
# 			elif board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):	# Temp board since we need to look one step forward for gives_check (ie does next move take king)
# 				check_moves.append((src_row, src_col, dest_row, dest_col))
# 			else:
# 				remaining_moves.append((src_row, src_col, dest_row, dest_col))

# 			# if board.is_capture(src_row, src_col, dest_row, dest_col):
# 			# 	capture_moves.append((src_row, src_col, dest_row, dest_col)) # Filters capture moves
# 			# elif board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
# 			# 	check_moves.append((src_row, src_col, dest_row, dest_col))  # Filters check-giving moves
# 			# else:
# 			# 	remaining_moves.append((src_row, src_col, dest_row, dest_col)) # Remaining moves are stored for random gameplay in worst case of policy

# 	return capture_moves, check_moves, remaining_moves 
# 	# Moves are listed in priority order


# def smartest_move_MCTS(board:RawChessBoard, color):
# 	capture_moves, check_moves, remaining_moves = get_moves_MCTS(board, color) # Get moves in priority order for black player

# 	# Random selection implemented in hierarchal categorical order. Randomisation prevents local maxima (eg: rook repitition observed)
# 	if len(capture_moves) != 0:
# 		best_move = choice(capture_moves)
# 	elif len(check_moves) != 0:
# 		best_move = choice(check_moves)
# 	elif len(remaining_moves) != 0:
# 		best_move = choice(remaining_moves)
# 	else:
# 		print("LINE262; No valid moves available for MCTS agent of color {0}".format(color))
# 		return None
	
# 	return best_move


# def convert_moves_format(moves:list) -> list:
# 	usable_moves = []

# 	for move in moves:
# 		src_row, src_col = move["row"], move["col"]

# 		for dest_row, dest_col in move["moves"]:
# 			usable_moves.append((src_row, src_col, dest_row, dest_col))
	
# 	return usable_moves


# # ---------------------------------------- CODE GRAVEYARD --------------------------------------------------

# 		# all_available_moves = self.board.get_playable_moves(self.color)

# 		# # Initialisation of move arrays
# 		# capture_moves = []
# 		# check_moves = []
# 		# remaining_moves = []
# 		# opp_color = 'black' if self.color == 'white' else 'white' # gives_check takes opponent color

# 		# # Converts moves from dict into target usable format
# 		# for move in all_available_moves:
# 		# 	src_row, src_col = move["row"], move["col"]

# 		# # Evaluate possible moves from source coordinate
# 		# # Check for captures, then check for check-giving moves -> Update arrays
# 		# 	for dest_coordinates in move["moves"]:
# 		# 		dest_row, dest_col = dest_coordinates
# 		# 		if self.board.is_capture(src_row, src_col, dest_row, dest_col):
# 		# 			capture_moves.append((src_row, src_col, dest_row, dest_col)) # Filters capture moves
# 		# 		elif self.board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
# 		# 			check_moves.append((src_row, src_col, dest_row, dest_col))  # Filters check-giving moves
# 		# 		else:
# 		# 			remaining_moves.append((src_row, src_col, dest_row, dest_col)) # Remaining moves are stored for random gameplay in worst case of policy

# 		# return capture_moves + check_moves + remaining_moves 
# 		# # Moves are listed in priority order

# 	# state = RawChessBoard(
# 	# 	board=copy.deepcopy(board_arg.board),
# 	# 	number_of_total_moves=board_arg.number_of_total_moves,
# 	# 	game_status=board_arg.game_status
# 	# )

# # next_state = state.get_state_after_move(move[0], move[1], move[2], move[3]) # Get new board state after making this move; will be used as board state for next iteration of simulation

# # if current_player != self.color: # Game ends on opponent's turn (ie player forced checkmate/stalemate ie win)
# # 	return 1 
# # else:  
# # 	return 0 

# # raise Exception("No valid moves available for agent of color {0}".format(self.color))

from random import choice
from board import RawChessBoard, ChessBoardGUI
import copy
import math

import board

#TODO: Optimise/abide by chess rules: White does not move king when in check. Chess rules dictate that a player in check MUST move out of check, so long as a move exists to exit check (ie: not a checkmate case)

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
		
        #CHANGE
		self.capture_moves, self.check_moves, self.other_moves = self.get_all_moves()
		# self.remaining_moves = self.get_all_moves() # List of all moves that can be made from this node's board state; used for expansion


	def get_all_moves(self):
		return get_moves_MCTS(self.board, self.color)
	

	def is_fully_expanded(self):
		#CHANGE
		return len(self.capture_moves == 0 and self.check_moves == 0 and self.other_moves == 0)
		# return len(self.remaining_moves) == 0 # Node fully expanded iff no remaining moves left to expand
	
	
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
	def select(self, node:Node) -> Node :
		# STAGE 1: SELECTION (pick best node to explore based on UCB score)
		while node.is_fully_expanded() and len(node.children) > 0: # Want current node to be expanded, but children to exist to select from
			node = node.choose_best_child() # Pick best child node to explore based on UCB score
		return node
			
		
	# CHANGED: expand
	def expand(self, node:Node) -> Node :
		board = node.board # Board state of current node
		# STAGE 2: EXPANSION (expand node by adding child node corresponding to move selected from remaining moves)
		
        
        #CHANGE
		if len(node.capture_moves) == 0:
			next_move = choice(node.capture_moves)
			node.capture_moves.remove(next_move)
		elif len(node.check_moves) == 0:
			next_move = choice(node.check_moves)
			node.check_moves.remove(next_move)
		elif len(node.other_moves) == 0:
			next_move = choice(node.other_moves)
			node.other_moves.remove(next_move)        
		else:
			return node
		
		# Next state -- Type: 2D list
		new_board_state = board.get_state_after_move(node.color, src_row, src_col, dest_row, dest_col) # Get new board state after making this move; will be used as board state for child node

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
	



	def simulate(self, board_arg:RawChessBoard, color) -> int:
		# STAGE 3: SIMULATION (play out game from this child node using playout policy; return result of playout)
		
		# Copy of board so original board is not modified during simulation
		# Uses deepcopy on the underlying board
		simulation_board = copy.deepcopy(board_arg)

		current_player = color

		for ply in range(board.MAX_NUM_PLY):

			# Break is game is already done
			if simulation_board.is_terminal(current_player) or simulation_board.is_king_in_checkmate(current_player):
				break
			
			if current_player == "white":
				# White player: Random (unintelligent) play
				move = random_move(self, simulation_board, current_player) # Random move selection for white player. Explicitly passes white as colour, since self (MCTS agent) is black

			else:
				# Black player: Playout policy (intelligent)
				move = smartest_move_MCTS(simulation_board, current_player)

			# Break if no moves available for current player (ie checkmate/stalemate)
			if move is None: 	# None logic implemented in random_move (for white) and smartest_move_MCTS (for black)
				break

			# Simulate gameplay
			# next_state = state.get_state_after_move(move[0], move[1], move[2], move[3]) # Get new board state after making this move; will be used as board state for next iteration of simulation
			simulation_board.move_piece(current_player, move[0], move[1], move[2], move[3]) # Update state of board to reflect simulated move (ie make the move on the board)
			# print("LINE 152: Simulation move made: player was", current_player, ". move was", move)

			# Players change turns
			current_player = 'black' if current_player == 'white' else 'white'


		# # Copy of board so original board is not modified during simulation
		# # Uses deepcopy on the underlying board
		# simulation_board = copy.deepcopy(board_arg)

		# # state = RawChessBoard(
		# # 	board=copy.deepcopy(board_arg.board),
		# # 	number_of_total_moves=board_arg.number_of_total_moves,
		# # 	game_status=board_arg.game_status
		# # )

		# current_player = color

		# for ply in range(board.MAX_NUM_PLY):

		# 	# Break is game is already done
		# 	if simulation_board.is_terminal(current_player) or simulation_board.is_king_in_checkmate(current_player):
		# 		break
			
		# 	if current_player == "white":
		# 		# White player: Random (unintelligent) play
		# 		move = random_move(self, simulation_board, current_player) # Random move selection for white player. Explicitly passes white as colour, since self (MCTS agent) is black

		# 	else:
		# 		# Black player: Playout policy (intelligent)
		# 		move = smartest_move_MCTS(simulation_board, current_player)

		# 	# Break if no moves available for current player (ie checkmate/stalemate)
		# 	if move is None: 	# None logic implemented in random_move (for white) and smartest_move_MCTS (for black)
		# 		break

		# 	# Simulate gameplay
		# 	# next_state = state.get_state_after_move(move[0], move[1], move[2], move[3]) # Get new board state after making this move; will be used as board state for next iteration of simulation
		# 	simulation_board.move_piece(current_player, move[0], move[1], move[2], move[3]) # Update state of board to reflect simulated move (ie make the move on the board)
		# 	# print("LINE 152: Simulation move made: player was", current_player, ". move was", move)

		# 	# Players change turns
		# 	current_player = 'black' if current_player == 'white' else 'white'

		# # Eval function @ end of (simulated) game
		# if simulation_board.is_king_in_checkmate(self.opponent): # If opponent is in checkmate, this is a win for the MCTS agent
		# 	return 1
		# elif simulation_board.is_king_in_checkmate(self.color): # If MCTS agent is in checkmate, this is a loss for the MCTS agent
		# 	return 0
		# else:
		# 	return 0 	# Should only occur if max ply is exceeded before checkmate

		# # if current_player != self.color: # Game ends on opponent's turn (ie player forced checkmate/stalemate ie win)
		# # 	return 1 
		# # else:  
		# # 	return 0 


	def backpropagate(self, node:Node, result:int):
		# STAGE 4: BACKPROPAGATION (update win/visit counts along path from child to root based on result of simulation playout)
		while node is not None:		# Terminates after root case (root.parent = None)
			node.visits += 1
			node.wins += result
			node = node.parent 		# Upwards traversal until root


	def get_next_move(self, gameboard:ChessBoardGUI): #must return src_row, src_col, dest_row, dest_col
		root = Node(copy.deepcopy(gameboard.uboard), color=self.color) # Create root node for MCTS tree with current board state and agent's color
		# Deepcopy to avoid manipulating actual game board during MCTS; once next_move is returned, THEN real gameboard updated in main.py
		for _ in range(100):
			leaf:Node = self.select(root)
			child:Node = self.expand(leaf)
			result = self.simulate(child.board, child.color)
			self.backpropagate(child, result)
		
		best_child:Node = max(root.children, key=lambda c: c.visits) # Picks child with most visits -- ie best child
		print("LINE 188: best_child move is", best_child.move, "with", best_child.visits, "visits and", best_child.wins, "wins")
		return best_child.move # Return move corresponding to best child
		# return random_move(self, gameboard.uboard, self.color) # TESTING ONLY. COMMENT ABOVE, COMMENT HERE AS NEEDED

class RandomChessAgent(object):
	def __init__(self, color):
		self.color = color

	# Main logic for MCTS agent
	def get_next_move(self, gameboard:ChessBoardGUI, is_init=False): #must return src_row, src_col, dest_row, dest_col
		return random_move(self, gameboard.uboard, self.color) # Random move selection for random chess agent; also used for MCTS agent if no captures or check-giving moves are available
	

# HELPER FUNCTIONS
def random_move(agent: MonteCarloChessAgent | RandomChessAgent, board:RawChessBoard, color):
	# Random Chess Agent acts randomly -- random piece selection, random move selection from that piece's available moveset
	# MCTS Agent does NOT act randomly, but needs random move selection if no captures or check-giving moves are available. Can use this function in that case.
	
	all_available_moves = board.get_playable_moves(color)	# Gets all playable moves at given state of the board for the agent's color

	# Account for cases where moves are not possible (avoid IndexError from choice() function)
	# Filters invalid moves
	valid_moves = [mv for mv in all_available_moves if len(mv["moves"]) > 0]
	if len(valid_moves) == 0:
		# raise Exception("No valid moves available for agent of color {0}".format(self.color))
		return None 	# No plays available

	# Random selection of moves
	selected_piece_moves = choice(valid_moves)		# Randomly selects a piece, as well as all its move choices
	selected_move = choice(selected_piece_moves["moves"])	# Randomly selects a move from the selected piece's move choices
	return selected_piece_moves["row"], selected_piece_moves["col"], selected_move[0], selected_move[1]
	#NB: selected_piece moves dict contains row & col (initial position of selected piece); selected_move is a tuple containing new row and new col (in that order)


def get_UCB(node:Node, c=1.41):
	if node.visits == 0 or node.parent is None: # Unvisited & root node cases
		return float('inf')  # Return positive infinity; forces exploration of unvisited nodes
	
	# UCB Formula
	exploit = node.wins / node.visits
	explore = c * math.sqrt(math.log(node.parent.visits) / node.visits)
	return exploit + explore


def get_moves_MCTS(board:RawChessBoard, color):
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
			if board.is_capture(src_row, src_col, dest_row, dest_col):
				capture_moves.append((src_row, src_col, dest_row, dest_col)) # Filters capture moves
			elif board.gives_check(src_row, src_col, dest_row, dest_col, opp_color):
				check_moves.append((src_row, src_col, dest_row, dest_col))  # Filters check-giving moves
			else:
				remaining_moves.append((src_row, src_col, dest_row, dest_col)) # Remaining moves are stored for random gameplay in worst case of policy

	return capture_moves + check_moves + remaining_moves 
	# Moves are listed in priority order


def smartest_move_MCTS(board:RawChessBoard, color):
	moves = get_moves_MCTS(board, color) # Get moves in priority order for black player
	if len(moves) == 0:
		print("LINE262; No valid moves available for MCTS agent of color {0}".format(color))
		return None # Game over case (checkmate/stalemate for MCTS agent)
	
	best_move = moves[0] # Select best move based on playout policy logic (since moves are in priority order, best move is first move in list)
	# print("LINE 266: best_move is", best_move)
	return best_move # , moves # Best move returned + remaining moves returned



# GY

# if not node.remaining_moves:
# 	return node # If true, no moves to expand and current node is a leaf/terminal node. Can simply return this node.

# # Pick next move to expand from movelist (in priority order)
# next_move = node.remaining_moves.pop(0) # Get next move to expand; remove mv from movelist
# src_row, src_col, dest_row, dest_col = next_move

# # Next state -- Type: 2D list
# new_board_state = board.get_state_after_move(node.color, src_row, src_col, dest_row, dest_col) # Get new board state after making this move; will be used as board state for child node

# # Expand new child
# child_board = RawChessBoard(
# 	board=copy.deepcopy(new_board_state),
# 	number_of_total_moves=board.number_of_total_moves + 1,	# increment steps made in deepcopy version of game
# 	game_status=board.game_status
# )

# child = Node(
# 	board=child_board,
# 	color='black' if node.color == 'white' else 'white', # Child node = opposing color
# 	parent=node,
# 	move=next_move
# )

# node.children.append(child) # Add this new child to the list of children of the current node
# return child # Return child node (just expanded)