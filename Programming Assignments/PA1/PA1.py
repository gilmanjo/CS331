import sys


class PuzzleState(object):
	"""container for the state of the wolves and chickens puzzle

	Attributes:
		lb_chickens - number of chickens on the left bank
		rb_chickens - number of chickens on the right bank
		lb_wolves - number of wolves on the left bank
		rb_wolves - number of wolves on the right bank
		boat_left - boolean, is True if boat is on left bank, else on right
		"""
	def __init__(self):
		super(PuzzleState, self).__init__()
		self.lb_chickens = 0
		self.rb_chickens = 0
		self.lb_wolves = 0
		self.rb_wolves = 0
		self.boat_left = True

	def print_puz_state(self, fancy=False):
		"""prints the state of the puzzle to terminal

		Args:
			fancy - if True, prints in nicer-looking format

		Returns:
			(none)

		Raises:
			(none)
		"""
		if fancy:
			# TODO: implement fancy printing for easier debugging
			pass

		else:
			print("{},{},{}\n{},{},{}".format(
				self.lb_chickens,
				self.lb_wolves,
				0 if not self.boat_left else 1,
				self.rb_chickens,
				self.rb_wolves,
				0 if self.boat left, else 1))
		
def main():
	pass

def load_puz_state(fn):
	"""loads a text file as an initial state of the problem
	
	Args:
		fn - filepath to .txt file containing initial puzzle state

	Returns:
		fully initialized PuzzleState object

	Raises:
		(none)
	"""
	raw_data = []
	with open(fn, "r") as f:
		for line in f:
			raw_data.append(line.split(","))

	new_ps = GameState()
	new_ps.lb_chickens = raw_data[0][0]
	new_ps.rb_chickens = raw_data[1][0]
	new_ps.lb_wolves = raw_data[0][1]
	new_ps.lb_wolves = raw_data[1][1]

	# set boat_left boolean to False if the boat is on the right bank
	if raw_data[0][2] == 0:
		new_ps.boat_left = False

	return new_ps

if __name__ == '__main__':
	main()