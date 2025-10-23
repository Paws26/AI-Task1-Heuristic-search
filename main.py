import copy
import time
import heapq
import random

# Heuristic search 8-Puzzle solver

# Final position
puzzle_goal = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]

class Node:
    def __init__(self, puzzle_state, parent=None, g_cost=0, h_cost=0):
        self.puzzle_state = puzzle_state
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    # Always return the node with smallest f-cost
    def __lt__(self, other):
        return self.f_cost < other.f_cost

# Generate a specified amount of puzzle nodes
def generate_puzzle_nodes(amount):
    puzzle_nodes_start = []
    while amount > 0:
        new_state = []
        nums = random.sample(range(0,9), 9)
        for j in range(0, 3):
            new_state.append(nums[j::3])
        # Try again if state is not solvable
        if not check_for_solvability(new_state):
            continue
        new_node = Node(puzzle_state=new_state, parent=None, g_cost=0, h_cost=get_heuristic_value_manhatten(new_state))
        puzzle_nodes_start.append(new_node)
        amount -= 1
    return puzzle_nodes_start

# Confirm solvability of a puzzle state
def check_for_solvability(start_state):
    inversions = 0

    list_to_check = []
    for i in start_state:
        for j in i:
            list_to_check.append(j)

    list_to_check.remove(0)

    for i in range(len(list_to_check)):
        for j in range(i+1, len(list_to_check)):
            if list_to_check[i] > list_to_check[j]:
                inversions += 1

    if inversions % 2:
        return False
    else:
        return True


### Returns total heuristic value (h)
def get_heuristic_value_manhatten(puzzle_state):
    distance = 0
    for x in range(3):
        for y in range(3):
            puzzle_tile = puzzle_state[x][y]
            goal_x = 0
            goal_y = 0
            if puzzle_tile != 0:

                for dist_x in range(3):
                    for dist_y in range(3):
                        if puzzle_tile == puzzle_goal[dist_x][dist_y]:
                            goal_x = abs(dist_x - x)
                            goal_y = abs(dist_y - y)
                            break

            distance += goal_x + goal_y
    return distance

# Returns all states from a node which returns
# a valid new puzzle state after the blank moves
def get_next_nodes(node):
    next_nodes = []

    puzzle_state = node.puzzle_state

    for x in range(3):
        for y in range(3):
            if puzzle_state[x][y] == 0:
                blank_x = x
                blank_y = y

    moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    for move_x, move_y in moves:
        new_x = blank_x + move_x
        new_y = blank_y + move_y

        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(puzzle_state)

            new_state[blank_x][blank_y] = new_state[new_x][new_y]
            new_state[new_x][new_y] = 0

            next_nodes.append(new_state)

    return next_nodes

### A* Search Algorithm
def solve_puzzle(node):
    start_node = node

    open_list = [start_node]

    # Set for already searched Puzzle states
    closed_set = set()

    # Create queue for nodes
    heapq.heapify(open_list)

    while open_list is not None:
        # Take node from the queue with lowest f-cost
        current_node = heapq.heappop(open_list)

        # Check if node is already at goal state
        if current_node.puzzle_state == puzzle_goal:
            return current_node

        # If state was already searched, continue
        current_state_tuple = tuple(map(tuple, current_node.puzzle_state))
        if current_state_tuple in closed_set:
            continue

        # Get successor states
        successor_states = get_next_nodes(current_node)

        # Add state of node to already searched puzzle states
        closed_set.add(current_state_tuple)

        for successor_state in successor_states:
            successor_node = Node(puzzle_state=successor_state,
                                  parent=current_node,
                                  g_cost=current_node.g_cost + 1,
                                  h_cost=get_heuristic_value_manhatten(successor_state))
            heapq.heappush(open_list, successor_node)

    return None

# Initial Nodes
puzzle_nodes = generate_puzzle_nodes(100)

start_time = time.time()

count = 1
for puzzle_node in puzzle_nodes:
    solved_node = solve_puzzle(puzzle_node)
    print(f"Solved nr. {count}")
    count = count + 1

finish_time = time.time()
elapsed_time = finish_time - start_time
print(f"Solving took {elapsed_time} seconds")


### Print results
'''
print("Original State:")
for row in start_node.puzzle_state:
    print(row)

print("Is this puzzle solvable?", check_for_solvability(start_node))

solution_node = solve_puzzle(start_node)



if solution_node:
    print("Solution found:")
    
    for row in solution_node.puzzle_state:
        print(row)
    print("---")
    

    path = []
    current_node = solution_node

    while current_node is not None:
        path.append(current_node.puzzle_state)
        current_node = current_node.parent

    path.reverse()

    print(f"Solved in {len(path)} steps.")
    for i, state in enumerate(path):
        print(f"Move {i}")
        for row in state:
            print(row)
        print("---")
else:
    print("No solution found")

print(generate_puzzle_state(10))
'''