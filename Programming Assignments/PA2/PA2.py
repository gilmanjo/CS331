import copy
from enum import Enum
import numpy as np
import random
import sys


# Constants
BOARD_WIDTH = 4
BOARD_HEIGHT = 4


class Piece(Enum):
	BLACK = 0
	WHITE = 1

class GameDriver(object):
	"""High-level logic for Othello game

	Attributes:
		board - Board object containing game grid
		p1 - Player object controlling dark pieces
		p2 - Player object controlling white pieces
		result - string detailing game outcome or current game state
		consec_no_moves - number of consecutive player turns where there were
			no valid moves
	"""
	def __init__(self, max_player, min_player):
		super(GameDriver, self).__init__()

		self.board = Board()
		self.p1 = HumanPlayer("X") if max_player is 0 else MinimaxPlayer("X")
		self.p2 = HumanPlayer("O") if min_player is 0 else MinimaxPlayer("O")
		self.result = "Game is in progress"
		self.consec_no_moves = 0

	def player_move(self, p_num):
		"""Player makes a move

		If human, a move will be prompted to screen, otherwise the minimax
		algorithm will be invoked to generate a move for AI player.

		Args:
			p_num - the player number who will make a move

		Returns:
			(none)

		Raises:
			IndexError if p_num isn't 1 or 2
		"""
		if p_num < 1 or p_num > 2:
			raise IndexError("No such player.")

		player = getattr(self, "p{}".format(p_num))

		if type(player) is HumanPlayer:
			
			while(True):

				# get a list of moves the player can make
				valid_moves = self.collect_valid_moves(self.board,
					player.token)

				# if the player has no valid moves, skip their turn
				if len(valid_moves) == 0:
					print_game_message(
						"Player {} has no valid moves!".format(p_num))
					self.consec_no_moves += 1
					break

				# print possible moves
				for idx, move in enumerate(valid_moves):
					print("[{}]\tRow {}\tColumn {}\tCapture {} pieces".format(
						idx + 1, move.x, move.y, len(move.bounded_pieces)))

				# collect player's choice
				choice = int(input("\nSelect a move:"))

				# error check player's input
				if choice > 0 and choice <= len(valid_moves):
					self.board.make_move(valid_moves[choice-1])
					self.consec_no_moves = 0
					break

				print_game_message("Invalid choice.  Try again.")

		else:

			# get a list of moves the player can make
			valid_moves = self.collect_valid_moves(self.board,
				player.token)

			# if the player has no valid moves, skip their turn
			if len(valid_moves) == 0:
				print_game_message(
					"AI Player {} has no valid moves!".format(p_num))
				self.consec_no_moves += 1
				return

			print_game_message("AI Player {} is making a decision...".format(
				p_num))
			move = self.minimax_decision(self.board, player.token)
			print_game_message(
				"AI Player {} places a piece at {}, {} and captures {} pieces.".format(
					p_num, move.x, move.y, len(move.bounded_pieces)))
			self.board.make_move(move)

	def collect_valid_moves(self, game_board, piece):
		"""Collects all valid moves for the given player color

		Args:
			game_board - game state to iterate through for valid moves
			piece - Piece enum representing palyer color

		Returns:
			a list of every possible Move object

		Raises:
			(none)
		"""
		valid_moves = []
		for x in range(game_board.grid.shape[0]):
			for y in range(game_board.grid.shape[1]):

				result = game_board.determine_valid_move(x, y, piece)
				if result == 1:
					continue
				else:
					valid_moves.append(Move(x, y, piece, result))

		return valid_moves

	def is_stable_piece(self, x, y, game_board):
		"""Determines if the given piece is stable

		Args:
			x - x-coordinate of piece to be checked
			y - y-coordinate of piece to be checked
			game_board - game state to check

		Returns:
			1 if stable
			0 if unstable

		Raises:
			(none)
		"""
		# check row and column
		for i in range(game_board.grid.shape[0]):

			if game_board.grid[x][i] == " " \
				or game_board.grid[i][y] == " ":
				return 0

		# check each of the four diagonals
		dx = 1
		dy = 1

		
		while(x+dx >= 0 and x+dx < game_board.grid.shape[0] \
			and y+dy >= 0 and y+dy < game_board.grid.shape[1]):

			if game_board.grid[x+dx][y+dy] == " ":
				return 0

			dx += 1
			dy += 1

		dx = -1
		dy = -1

		
		while(x+dx >= 0 and x+dx < game_board.grid.shape[0] \
			and y+dy >= 0 and y+dy < game_board.grid.shape[1]):

			if game_board.grid[x+dx][y+dy] == " ":
				return 0

			dx += -1
			dy += -1

		dx = -1
		dy = 1

		
		while(x+dx >= 0 and x+dx < game_board.grid.shape[0] \
			and y+dy >= 0 and y+dy < game_board.grid.shape[1]):

			if game_board.grid[x+dx][y+dy] == " ":
				return 0

			dx += -1
			dy += 1

		dx = 1
		dy = -1

		
		while(x+dx >= 0 and x+dx < game_board.grid.shape[0] \
			and y+dy >= 0 and y+dy < game_board.grid.shape[1]):

			if game_board.grid[x+dx][y+dy] == " ":
				return 0

			dx += 1
			dy += -1

		return 1

	def utility(self, game_board):
		"""Used to evaluate utility of a game position

		The MAX player seeks to maximize utility while the MIN player
		seeks to minimize it, for any given game state.  The utility
		will be defined as the point differential of the board.

		Args:
			game_board - Board object game state to analyze

		Returns:
			utility score of the game board

		Raises:
			(none)
		"""
		util = 0
		p1_num_tks = 0
		p2_num_tks = 0
		p1_num_moves = len(self.collect_valid_moves(game_board, Piece.BLACK))
		p2_num_moves = len(self.collect_valid_moves(game_board, Piece.WHITE))
		p1_num_corners = 0
		p2_num_corners = 0
		p1_num_stable_tks = 0
		p2_num_stable_tks = 0

		for x in range(game_board.grid.shape[0]):
			for y in range(game_board.grid.shape[1]):

				if game_board.grid[x][y] == "X":

					p1_num_tks += 1

					# determine if this is a corner
					if (x == game_board.grid.shape[0] - 1 
						and y == game_board.grid.shape[1] - 1) \
						or (x == 0 and y == game_board.grid.shape[1] - 1) \
						or (x == game_board.grid.shape[0] - 1 and y == 0) \
						or (x == 0 and y == 0):
						p1_num_corners += 1
						p1_num_stable_tks += 1

					elif self.is_stable_piece(x, y, game_board):
						p1_num_stable_tks += 1

				elif game_board.grid[x][y] == "O":

					p2_num_tks += 1

					# determine if this is a corner
					if (x == game_board.grid.shape[0] - 1 
						and y == game_board.grid.shape[1] - 1) \
						or (x == 0 and y == game_board.grid.shape[1] - 1) \
						or (x == game_board.grid.shape[0] - 1 and y == 0) \
						or (x == 0 and y == 0):
						p2_num_corners += 1
						p2_num_stable_tks += 1

					elif self.is_stable_piece(x, y, game_board):
						p2_num_stable_tks += 1

		# first heuristic: dominance of piece placement
		try:
			util += (p1_num_tks - p2_num_tks)/(p1_num_tks + p2_num_tks)

		except ZeroDivisionError:
			pass

		# second heuristic: number of available moves
		try:
			util += (p1_num_moves - p2_num_moves)/(p1_num_moves + p2_num_moves)

		except ZeroDivisionError:
			pass

		# third heuristic: number corners owned
		try:
			util += (p1_num_corners - p2_num_corners)/ \
				(p1_num_corners + p2_num_corners)

		except ZeroDivisionError:
			pass

		# fourth heuristic: number of stable pieces
		try:
			util += (p1_num_stable_tks - p2_num_stable_tks)/ \
				(p1_num_stable_tks + p2_num_stable_tks)

		except ZeroDivisionError:
			pass

		return util

	def successors(self, game_board, piece):
		"""Takes current game state and generates all succesors within 1 move

		Args:
			game_board - game state to generate successors for
			piece - Piece enum representing player color

		Returns:
			a list of 2-tuples containing a move and the corresponding
			state

		Raises:
			(none)
		"""
		valid_moves = self.collect_valid_moves(game_board, piece)
		s_list = []

		for move in valid_moves:
			new_game_board = copy.deepcopy(game_board)
			new_game_board.make_move(move)
			s_list.append((move, new_game_board))

		return s_list

	def minimax_decision(self, game_board, piece):
		"""Performs Minimax algorithm for AI and returns AI's move

		Args:
			game_board - game state of the AI player's turn
			piece - Piece enum corresponding to AI player's color

		Returns:
			move - the move that the AI player selects

		Raises:
			(none)
		"""
		if piece == Piece.BLACK:
			val = self.max_value(game_board)
			print_game_message("Move utility: {}".format(val))

			for move, state in self.successors(game_board, Piece.BLACK):
				if val == self.max_value(game_board):
					return move

		else:
			val = self.min_value(game_board)
			print_game_message("Move utility: {}".format(val))

			for move, state in self.successors(game_board, Piece.WHITE):
				if val == self.min_value(game_board):
					return move

	def max_value(self, game_board):
		"""Recursive function finds the maximum value for the provided state

		Args:
			game_board - the current game state

		Returns:
			val - the maximum value of the current state

		Raises:
			(none)
		"""
		valid_moves = self.collect_valid_moves(game_board, Piece.BLACK)

		# base case
		if len(valid_moves) == 0:
			return self.utility(game_board)

		val = -np.inf
		for move, state in self.successors(game_board, Piece.BLACK):
			val = max(val, self.min_value(state))

		return val

	def min_value(self, game_board):
		"""Recursive function finds the minimum value for the provided state

		Args:
			game_board - the current game state

		Returns:
			val - the minimum value of the current state

		Raises:
			(none)
		"""
		valid_moves = self.collect_valid_moves(game_board, Piece.WHITE)

		# base case
		if len(valid_moves) == 0:
			return self.utility(game_board)

		val = np.inf
		for move, state in self.successors(game_board, Piece.WHITE):
			val = min(val, self.max_value(state))

		return val

	def calculate_winner(self):
		"""Tallies up the number of pieces for each player

		Args:
			(none)

		Returns:
			(none)

		Raises:
			(none)
		"""
		p1_s = 0
		p2_s = 0
		for x in range(self.board.grid.shape[0]):
			for y in range(self.board.grid.shape[1]):

				if self.board.grid[x][y] == "X":
					p1_s += 1
				elif self.board.grid[x][y] == "O":
					p2_s += 1

		if p1_s > p2_s:
			self.result = "Player 1 wins! {}-{}".format(p1_s, p2_s)
		elif p2_s > p1_s:
			self.result = "Player 2 wins! {}-{}".format(p2_s, p1_s)
		else:
			self.result = "Tie game!  {}-{}".format(p1_s, p2_s)

	def game_over(self):
		"""Check if the game has ended

		Args:
			(none)

		Returns:
			True if at least two turns without placement have occurred
			False otherwise

		Raises:
			(none)
		"""
		if self.consec_no_moves >= 2:
			self.calculate_winner()
			return True
		else:	
			return False
		
class Player(object):
	"""Abstract class for Player objects

		Attributes:
			token - Piece enum object signifying which color the player is
				using
	"""
	def __init__(self, token):
		super(Player, self).__init__()

		self.token = Piece.BLACK if token == "X" else Piece.WHITE
		
class HumanPlayer(Player):
	"""docstring for HumanPlayer
	"""
	def __init__(self, token):
		super(HumanPlayer, self).__init__(token)
		
class MinimaxPlayer(Player):
	"""docstring for MinimaxPlayer
	"""
	def __init__(self, token):
		super(MinimaxPlayer, self).__init__(token)

	def get_move(self):
		pass
		
class Board(object):
	"""Grid for an Othello/Reversi board.

		Contains the grid of the game board and methods for adding pieces.

		Attributes:
			grid - a 2D numpy array of strings corresponding to the pieces
				on the board
	"""
	def __init__(self):
		super(Board, self).__init__()
		self.grid = np.array([[" ", " ", " ", " "],
			[" ", "O", "X", " "],
			[" ", "X", "O", " "],
			[" ", " ", " ", " "]])

	def determine_valid_move(self, x, y, piece):
		"""Adds a game piece to the board and adjusts the board state

		Args:
			x - the x-coordinate of the location to place a piece
			y - the y-coordinate of the location to place a piece
			piece - the Piece enum object of the color being placed

		Returns:
			0 if the move was successful, 1 if it was invalid

		Raises:
			ValueError if the piece argument is not passed correctly
		"""

		# check if space is already occupied
		if self.grid[x][y] != " ":
			return 1

		# check if token is being placed adjacent to an opposing piece and
		# if it is, we look to see if a bound can be found, adding all the
		# opponent's pieces inbetween to the turnover array
		turnover_pieces = []
		adj = False
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):

				# efficiency, skip the location we're currently trying to
				# place into
				if i == x and j == y:
					continue

				# check grid bounds to avoid indexing errors
				if i >= 0 and i < self.grid.shape[0] \
					and j >= 0 and j < self.grid.shape[1]:

					# if the piece in the current location is opposite of the
					# player placing a piece, look for bounds
					if (self.grid[i][j] == "X" and piece == Piece.WHITE) \
						or (self.grid[i][j] == "O" and piece == Piece.BLACK):
						
						# subtracting the difference between the center
						# location and the surrounding squares gives us
						# a relative position indicating a direction
						turnover_pieces += self.collect_bounded(
							x, y, i - x, j - y, piece)

		if len(turnover_pieces) == 0:
			return 1

		else:
			return turnover_pieces
			

	def collect_bounded(self, x, y, rx, ry, piece):
		"""Determines pieces bounded between opponent pieces

		Args:
			x - x-coordinate of the anchor bounding piece
			y - y-coordinate of the anchor bounding piece
			rx - relative x-direction to iterate in
			ry - relative y-direction to iterate in
			piece - Piece color to check for 2nd bound

		Returns:
			list of tuples of bounded pieces, or an empty list

		Raises:
			(none)
		"""
		# we will continue iterating in the direction dictated by rx and ry
		# until we reach a blank, the edge of the grid, or the placing piece
		bounded_pieces = []
		shift_x = rx
		shift_y = ry
		while(x + shift_x < self.grid.shape[0]
			and x + shift_x >= 0
			and y + shift_y < self.grid.shape[1]
			and y + shift_y >= 0
			and self.grid[x+shift_x][y+shift_y] != " "):
		
			if (self.grid[x+shift_x][y+shift_y] == "X" \
				and piece == Piece.BLACK) \
				or (self.grid[x+shift_x][y+shift_y] == "O" \
				and piece == Piece.WHITE):

				return bounded_pieces

			bounded_pieces.append((x+shift_x, y+shift_y))

			shift_x += rx
			shift_y += ry

		# if we never reached a second bounding piece, return empty list
		return []

	def make_move(self, move):
		"""Applies a Move object to the game board and changes game state

		Args:
			move - Move object with coordinates of move, piece to place,
				and bounded pieces to convert

		Returns:
			(none)

		Raises:
			ValueError if the piece argument of the Move object is invalid
		"""
		for bounded_piece in move.bounded_pieces:
				if move.piece == Piece.BLACK:
					self.grid[bounded_piece[0]][bounded_piece[1]] = "X"
				else:
					self.grid[bounded_piece[0]][bounded_piece[1]] = "O"

		if move.piece == Piece.BLACK:
			self.grid[move.x][move.y] = "X"

		elif move.piece == Piece.WHITE:
			self.grid[move.x][move.y] = "O"

		else:
			raise ValueError(
				"Piece argument must be Piece.BLACK or Piece.WHITE.")

	def print(self):
		"""Prints the board state to terminal

		Args:
			(none)

		Returns:
			(none)

		Raises:
			(none)
		"""
		for x in range(2*BOARD_WIDTH + 2):
			for y in range(2*BOARD_HEIGHT + 2):

				if x == 0 and y == 0:
					print(" ", end="", flush=True)

				elif x % 2 == 1 and y == 0:
					print("  ", end="", flush=True)

				elif x % 2 == 1 and y <= BOARD_WIDTH:
					print(" ---", end="", flush=True)

				elif y == 0 and x % 2 == 0 and x > 0:
					print("{} ".format(int(x/2)-1), end="", flush=True)

				elif x == 0 and y % 2 == 0 and y > 0:
					print("{}".format(int(y/2)-1), end="", flush=True)

				elif x == 0 and y % 2 == 1:
					print("   ", end="", flush=True)

				elif x % 2 == 0 and x != 0 and y % 2 == 1:
					print("|", end="", flush=True)

				elif x % 2 == 0 and y != 0:
					print(" {} ".format(self.grid[int(x/2) - 1][int(y/2) - 1]),
						end="", flush=True)

			print("\n", end="")

class Move(object):
	"""Container for a valid move a player may make

	Attributes:
		x - x-coordinate of location to place a piece
		y - y-coordinate of location to place a piece
		piece - Piece enum representing player color
		bounded_pieces - list of tuples of pieces to convert
	"""
	def __init__(self, x, y, piece, bounded_pieces):
		super(Move, self).__init__()
		self.x = x
		self.y = y
		self.piece = piece
		self.bounded_pieces = bounded_pieces
			
def main():
	
	max_player = 0 if sys.argv[1] == "human" else 1
	min_player = 0 if sys.argv[2] == "human" else 1

	game = GameDriver(max_player, min_player)
	print_game_message(
		"New Othello game beginning with {} player as X's and {} player as O's".format(
			sys.argv[1], sys.argv[2]))

	rd_num = 1
	while(not game.game_over()):

		print_game_message("Round {}".format(rd_num))
		game.board.print()
		print_game_message("Player 1's Move")
		game.player_move(1)
		game.board.print()
		print_game_message("Player 2's Move")
		game.player_move(2)

		rd_num += 1

	print_game_message("Game has ended.  {}!".format(game.result))

def print_game_message(message):
	"""Helper function for pretty printing of text messages

	Args:
		message - text message to print

	Returns:
		(none)

	Raises:
		(none)
	"""
	print("\n#####\n{}\n#####\n".format(message))

if __name__ == '__main__':
	main()