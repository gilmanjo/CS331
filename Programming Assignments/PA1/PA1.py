from enum import Enum
import sys


# Constants
NUM_ACTIONS = 5

class Action(Enum):
	ONE_CHICKEN = 0
	TWO_CHICKENS = 1
	ONE_WOLF = 2
	ONE_WOLF_ONE_CHICKEN = 3
	TWO_WOLVES = 4

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

class Node(object):
	"""represents a possible state and the result of some particular action,
	to be used as a data structure for finding an optimal solution

	Attributes:
		state - the puzzle state corresponding to this node
		parent - the parent of this node
		action - the action taken to reach the state of this node
		path_cost - the cost of all actions taken to reach the state of this
					node
	"""
	def __init__(self, ps, parent, action, cost=0):
		super(Node, self).__init__()
		self.state = ps
		self.parent = parent
		self.action = action
		self.path_cost = cost
		self.expanded = False

	def expand_node(self):
		"""expands the current node, if there are future states

		Returns:
			a list of nodes whose parent is the current node
		"""
		children = []
		for x in range(NUM_ACTIONS):

			new_node = Node(self.gen_ps(x), self, x, self.path_cost + 1)

			if self.is_valid_action(new_node.state):
				children.append(new_node)

		self.expanded = True
		return children

	def is_valid_action(self, ps):
		"""checks the puzzle state for evidence of an invalid action

		Compares the number of chickens to the number of wolves
		on each bank as there cannot be more wolves than chickens
		in any case.  Additionally, if the puzzle state has a negative value
		for any attribute, we have made a logic error in moving animals

		Args:
			ps - the puzzle state to check for validity

		Returns:
			True if the action is valid
		"""
		if ps.lb_chickens < 0 \
			or ps.rb_chickens < 0 \
			or ps.lb_wolves < 0 \
			or ps.rb_wolves < 0 \
			or ps.lb_chickens < ps.lb_wolves \
			or ps.rb_chickens < rb.wolves:

			return False

		return True

	def gen_ps(self, action):
		""" creates a new state based on the action applied

		Args:
			action - the action to apply to the state

		Returns:
			a new puzzle state based on the current node and new action

		Raises:
			ValueError if the action is not within the Action enumeration
		"""
		new_state = self.ps

		if action == Action.ONE_CHICKEN:
			
			if self.ps.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens -= 1
				new_state.rb_chickens += 1

			else:

				new_state.boat_left = True
				new_state.rb_chickens -= 1
				new_state.lb_chickens += 1

		elif action == Action.TWO_CHICKENS:
				
			if self.ps.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens -= 2
				new_state.rb_chickens += 2

			else:

				new_state.boat_left = True
				new_state.rb_chickens -= 2
				new_state.lb_chickens += 2

		elif action == Action.ONE_WOLF:
				
			if self.ps.boat_left:

				new_state.boat_left = False
				new_state.lb_wolves -= 1
				new_state.rb_wolves += 1

			else:

				new_state.boat_left = True
				new_state.rb_wolves -= 1
				new_state.lb_wolves += 1

		elif action == Action.ONE_WOLF_ONE_CHICKEN:
				
			if self.ps.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens -= 1
				new_state.rb_chickens += 1
				new_state.lb_wolves -= 1
				new_state.rb_wolves += 1

			else:

				new_state.boat_left = True
				new_state.rb_chickens -= 1
				new_state.lb_chickens += 1
				new_state.lb_wolves -= 1
				new_state.rb_wolves += 1

		elif action == Action.TWO_WOLVES:
				
			if self.ps.boat_left:

				new_state.boat_left = False
				new_state.lb_wolves -= 2
				new_state.rb_wolves += 2

			else:

				new_state.boat_left = True
				new_state.rb_wolves -= 2
				new_state.lb_wolves += 2

		else:
			raise(ValueError, "Invalid Action!")

		return new_state

	def print_path(self, fn=None):
		"""prints the complete history of actions leading to this node
		
		Args:
			fn - a filepath to a txt file to write the path

		Returns:
			(none)

		Raises:
			(none)
		"""
		action_history = []
		current_node = self

		# collect history
		while current_node.parent is not None:

			action_history.append(current_node.action)
			current_node = self.parent

		action_history.reverse()
		writeable_history = []

		# transform list of enums into writable text
		for idx, action in enumerate(action_history):

			if current_node.boat_left and idx % 2 == 0:

				writeable_history.append("Move {} to right bank".format(
					Action(action).name))

			else:

				writeable_history.append("Move {} to the left bank".format(
					Action(action).name))

		print(writeable_history)

		# if a filename was given, write the history to that file
		if fn is not None:
			with open(fn, "w") as f:
				f.writelines(writeable_history)

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