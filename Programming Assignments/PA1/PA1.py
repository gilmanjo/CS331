from copy import deepcopy
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

	def get_puzzle_state(self):
		"""returns a numerical representation of the puzzle state
		"""
		return "{}{}{}{}{}".format(self.lb_chickens,
									self.rb_chickens,
									self.lb_wolves,
									self.rb_wolves,
									self.boat_left)

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
				0 if self.boat_left else 1))

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
		self.state_history = [ps]
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

			new_node = Node(self.gen_ps(x), self, x, deepcopy(self.path_cost) + 1)
			if self.is_valid_action(new_node.state):
				new_node.state_history = new_node.parent.state_history + [new_node.state]
				children.append(new_node)

		self.expanded = True
		return children

	def is_valid_action(self, ps):
		"""checks the puzzle state for evidence of an invalid action

		Compares the number of chickens to the number of wolves
		on each bank as there cannot be more wolves than chickens
		in any case.  Additionally, if the puzzle state has a negative value
		for any attribute, we have made a logic error in moving animals.
		Finally it may not take the same action twice in a row.

		Args:
			ps - the puzzle state to check for validity

		Returns:
			True if the action is valid
		"""
		if int(ps.lb_chickens) < 0 \
			or int(ps.rb_chickens) < 0 \
			or int(ps.lb_wolves) < 0 \
			or int(ps.rb_wolves) < 0 \
			or (int(ps.lb_chickens) < int(ps.lb_wolves) and ps.lb_chickens > 0)\
			or (int(ps.rb_chickens) < int(ps.rb_wolves) and ps.rb_chickens > 0)\
			or self.is_in_state_history(self.state_history, ps):
			
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
		new_state = deepcopy(self.state)

		if action == Action.ONE_CHICKEN.value:
			
			if self.state.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens -= 1
				new_state.rb_chickens += 1

			else:

				new_state.boat_left = True
				new_state.rb_chickens = int(new_state.rb_chickens) - 1
				new_state.lb_chickens = int(new_state.lb_chickens) + 1

		elif action == Action.TWO_CHICKENS.value:
				
			if self.state.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens = int(new_state.lb_chickens) - 2
				new_state.rb_chickens = int(new_state.rb_chickens) + 2

			else:

				new_state.boat_left = True
				new_state.rb_chickens = int(new_state.rb_chickens) - 2
				new_state.lb_chickens = int(new_state.lb_chickens) + 2

		elif action == Action.ONE_WOLF.value:
				
			if self.state.boat_left:

				new_state.boat_left = False
				new_state.lb_wolves = int(new_state.lb_wolves) - 1
				new_state.rb_wolves = int(new_state.rb_wolves) + 1

			else:

				new_state.boat_left = True
				new_state.rb_wolves = int(new_state.rb_wolves) - 1
				new_state.lb_wolves = int(new_state.lb_wolves) + 1

		elif action == Action.ONE_WOLF_ONE_CHICKEN.value:
				
			if self.state.boat_left:

				new_state.boat_left = False
				new_state.lb_chickens = int(new_state.lb_chickens) - 1
				new_state.rb_chickens = int(new_state.rb_chickens) + 1
				new_state.lb_wolves = int(new_state.lb_wolves) - 1
				new_state.rb_wolves = int(new_state.rb_wolves) + 1

			else:

				new_state.boat_left = True
				new_state.rb_chickens = int(new_state.rb_chickens) - 1
				new_state.lb_chickens = int(new_state.lb_chickens) + 1
				new_state.lb_wolves = int(new_state.lb_wolves) + 1
				new_state.rb_wolves = int(new_state.rb_wolves) - 1

		elif action == Action.TWO_WOLVES.value:
				
			if self.state.boat_left:

				new_state.boat_left = False
				new_state.lb_wolves = int(new_state.lb_wolves) - 2
				new_state.rb_wolves = int(new_state.rb_wolves) + 2

			else:

				new_state.boat_left = True
				new_state.rb_wolves = int(new_state.rb_wolves) - 2
				new_state.lb_wolves = int(new_state.lb_wolves) + 2

		else:
			raise ValueError("Invalid Action!")

		return new_state

	def is_in_state_history(self, sh, ps):

		for state in sh:
			if state.get_puzzle_state() == ps.get_puzzle_state():
				return True

		return False

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
			current_node = current_node.parent

		action_history.reverse()
		writeable_history = []

		# transform list of enums into writable text
		for idx, action in enumerate(action_history):

			if current_node.state.boat_left and idx % 2 == 0 \
				or (not current_node.state.boat_left and idx % 2 == 1):

				writeable_history.append("Move {} to right bank\n".format(
					Action(action).name))

			else:

				writeable_history.append("Move {} to the left bank\n".format(
					Action(action).name))

		for line in writeable_history:
			print(line)

		# if a filename was given, write the history to that file
		if fn is not None:
			with open(fn, "w") as f:
				f.writelines(writeable_history)

def main():
	
	# assign command-line arguments
	input_state = load_puz_state(sys.argv[1])
	goal_state = load_puz_state(sys.argv[2])
	mode = sys.argv[3]
	output_file_loc = sys.argv[4]

	if mode == "bfs":
		bfs(input_state, goal_state, output_file_loc)

	elif mode == "dfs":
		dfs(input_state, goal_state, output_file_loc)

	elif mode == "iddfs":
		iddfs(input_state, goal_state, output_file_loc)

	elif mode == "astar":
		astar(input_state, goal_state, output_file_loc)

	else:
		raise ValueError("Invalid argument for mode!")

def bfs(input_state, goal_state, output_file_loc):
	
	# initialize queue with initial node from initial state
	queue = []
	explored = []
	initial_node = Node(input_state, None, None)
	queue.append(initial_node)

	while True:

		# exit if no solution was found
		if len(queue) == 0:
			with open(output_file_loc, "w") as f:
				f.write("No solution found.")
			break

		# pop a node from the front of the queue
		current_node = queue.pop(0)

		# check if node is our goal
		if is_goal_state(current_node, goal_state):
			current_node.print_path(output_file_loc)
			break

		# if not, expand
		queue += current_node.expand_node()  # add children to queue
		print("\ndepth: " + str(current_node.path_cost))
		explored.append(current_node)

def dfs(input_state, goal_state, output_file_loc):
	
	# initialize queue with initial node from initial state
	queue = []
	explored = []
	initial_node = Node(input_state, None, None)
	queue.append(initial_node)

	while True:

		# exit if no solution was found
		if len(queue) == 0:
			with open(output_file_loc, "w") as f:
				f.write("No solution found.")
			break

		# pop a node from the front of the queue
		current_node = queue.pop()

		# check if node is our goal
		if is_goal_state(current_node, goal_state):
			current_node.print_path(output_file_loc)
			break

		# if not, expand
		queue += current_node.expand_node()  # add children to queue
		print("\ndepth: " + str(current_node.path_cost))
		explored.append(current_node)

def iddfs(input_state, goal_state, output_file_loc):

	# continously increase the depth limit of our depth-first search
	depth = 0
	queue = []
	explored = []
	while True:

		print("\ndepth: {}".format(depth))

		# problem is a 3-tuple of format (node, queue, explored)
		problem = dls(input_state, goal_state, depth, queue, explored)
		queue = problem[1]
		explored = problem[2]

		# case all nodes have been expanded with no solution
		if problem[0] == -1:
			print("No solution found.")
			with open(output_file_loc, "w") as f:
				f.write("No solution found.")
			break

		# case all nodes at the depth limit have been expanded and there is
		# no solution, but deepest nodes may still be expanded
		elif problem[0] == 0:
			depth += 1

		# case the solution has been found
		else:
			problem[0].print_path(output_file_loc)
			break

def dls(input_state, goal_state, depth_limit, queue, explored):
	"""depth-limited search
	"""

	# initialize queue with initial node from initial state
	if len(queue) == 0 and len(explored) == 0:
		initial_node = Node(input_state, None, None)
		queue.append(initial_node)

	final_lvl = []  # the nodes is the deepest level of our limit

	while True:

		# exit if no solution was found
		if len(queue) == 0:
			return (-1, queue, explored)

		# pop a node from the front of the queue
		current_node = queue.pop()

		# check if node is our goal
		if is_goal_state(current_node, goal_state):
			return (current_node, queue, explored)

		# if not, check if we are allowed to expand
		if current_node.path_cost == depth_limit and len(queue) == 0:
			final_lvl.append(current_node)  # re-add current node
			return (0, final_lvl, explored)

		# saving the deepest level of our tree saves redunandcy in re-checking
		# all of the early, non-solution nodes
		elif current_node.path_cost == depth_limit:
			final_lvl.append(current_node)

		else:
			queue += current_node.expand_node()  # add children to queue
			explored.append(current_node)

def astar(input_state, goal_state, output_file_loc):
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
			raw_data.append(line.strip("\r\n").split(","))

	new_ps = PuzzleState()
	new_ps.lb_chickens = int(raw_data[0][0])
	new_ps.rb_chickens = int(raw_data[1][0])
	new_ps.lb_wolves = int(raw_data[0][1])
	new_ps.rb_wolves = int(raw_data[1][1])

	# set boat_left boolean to False if the boat is on the right bank
	if int(raw_data[0][2]) == 0:
		new_ps.boat_left = False

	return new_ps

def is_goal_state(node, gps):
	""" checks if the current node matches the puzzle state provided

	Args:
		node - Node object to be evaluated
		gps - goal puzzle state to compare with Node.state

	Returns:
		True if the states match

	Raises:
		(none)
	"""
	if node.state.lb_chickens == gps.lb_chickens \
		and node.state.rb_chickens == gps.rb_chickens \
		and node.state.lb_wolves == gps.lb_wolves \
		and node.state.lb_chickens == gps.lb_chickens:

		return True

	return False

if __name__ == '__main__':
	main()