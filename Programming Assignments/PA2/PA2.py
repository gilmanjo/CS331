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
	"""
	def __init__(self, max_player, min_player):
		super(GameDriver, self).__init__()

		self.board = Board()
		self.p1 = HumanPlayer("X") if max_player is 0 else MinimaxPlayer("X")
		self.p2 = HumanPlayer("O") if min_player is 0 else MinimaxPlayer("O")
		self.result = "Game is in progress"

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

				x = input("Enter the row of your move:")
				y = input("Enter the column of your move:")

				if self.board.add_piece(int(x), int(y), player.token) == 0:
					break

				print_game_message("Invalid move.  Try again.")

		else:
			print(player)

		input("")

	def game_over(self):
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

	def add_piece(self, x, y, piece):
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

		# check if token is being placed adjacent to an opposing piece
		adj = False
		for i in range(x - 1, x + 2):
			for j in range(y - 1, y + 2):

				# check grid bounds to avoid indexing errors
				if i >= 0 and i <= self.grid.shape[0] \
					and j >= 0 and j <= self.grid.shape[1]:

					if (self.grid[i][j] == "X" and piece == Piece.WHITE) \
						or (self.grid[i][j] == "O" and piece == Piece.BLACK):
						
						adj = True
						break

		if not adj:
			return 1

		# determine capture gaps
		#	check row
		for j in range(self.grid.shape[1]):

			if (self.grid[x][j] == "X" and piece == Piece.WHITE) \
				or (self.grid[i][j] == "O" and piece == Piece.BLACK):

				valid_gap = True

				for k in range(abs(y-j)):

					if (self.grid[x][j] == "X" and piece == Piece.BLACK) \
						or (self.grid[i][j] == "O" and piece == Piece.WHITE) \
						or (self.grid[i][j] == " "):

						valid_gap = False
						break

		if piece == Piece.BLACK:
			self.grid[x][y] = "X"

		elif piece == Piece.WHITE:
			self.grid[x][y] = "O"

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
		for x in range(1, 2*BOARD_WIDTH + 2):
			for y in range(1, 2*BOARD_HEIGHT + 2):

				if x % 2 == 1 and y <= BOARD_WIDTH:
					print(" ---", end="", flush=True)

				elif x % 2 == 0 and y % 2 == 1:
					print("|", end="", flush=True)

				elif x % 2 == 0:
					print(" {} ".format(self.grid[int(x/2) - 1][int(y/2) - 1]),
						end="", flush=True)

			print("\n", end="")
		
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
		game.player_move(1)
		game.board.print()
		game.player_move(2)

		rd_num += 1

	print_game_message("Game has ended.  {}!".format(game.result))

def utility():
	pass

def successor():
	pass

def minimax():
	pass

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