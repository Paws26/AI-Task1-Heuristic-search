import copy
import time
import heapq
import random
import statistics

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
    puzzle_nodes_manhattan = []
    puzzle_nodes_hamming = []
    while amount > 0:
        new_state = []
        nums = random.sample(range(0,9), 9)
        for j in range(0, 3):
            new_state.append(nums[j::3])
        # Try again if state is not solvable
        if not check_for_solvability(new_state):
            continue
        new_node_man = Node(puzzle_state=new_state,
                        parent=None,
                        g_cost=0,
                        h_cost=get_heuristic_value_manhattan(new_state))

        new_node_ham = Node(puzzle_state=new_state,
                        parent=None,
                        g_cost=0,
                        h_cost=get_heuristic_value_hamming(new_state))

        puzzle_nodes_manhattan.append(new_node_man)
        puzzle_nodes_hamming.append(new_node_ham)
        amount -= 1
    return puzzle_nodes_manhattan, puzzle_nodes_hamming

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


### Heuristic 1: Manhattan Distance
def get_heuristic_value_manhattan(puzzle_state):
    distance = 0
    for x in range(3):
        for y in range(3):
            puzzle_tile = puzzle_state[x][y]
            if puzzle_tile != 0:
                for dist_x in range(3):
                    for dist_y in range(3):
                        if puzzle_tile == puzzle_goal[dist_x][dist_y]:
                            distance += abs(dist_x - x) + abs(dist_y - y)
                            break
    return distance

# Heuristic 2: Hamming Distance
def get_heuristic_value_hamming(puzzle_state):
    distance = 0
    for x in range(3):
        for y in range(3):
            tile = puzzle_state[x][y]
            if tile != 0 and tile != puzzle_goal[x][y]:
                distance += 1
    return distance

# Get all valid states from a node after the blank moves
def get_next_nodes(node):
    next_nodes = []
    puzzle_state = node.puzzle_state

    # Find blank position
    for x in range(3):
        for y in range(3):
            if puzzle_state[x][y] == 0:
                blank_x = x
                blank_y = y

    # All possible moves
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
# Input: start node, heuristic function
# Output: solved node and number of expanded nodes
def solve_puzzle(node, heuristic_function):
    start_node = node
    open_list = [start_node]

    # Set for already searched Puzzle states
    closed_set = set()

    # Create queue for nodes
    heapq.heapify(open_list)

    # Counter for memory calculation
    expanded_nodes = 0

    while open_list:
        # Take node from the queue with lowest f-cost
        current_node = heapq.heappop(open_list)

        # Check if node is already at goal state
        if current_node.puzzle_state == puzzle_goal:
            return current_node, expanded_nodes

        # If state was already searched, continue
        current_state_tuple = tuple(map(tuple, current_node.puzzle_state))
        if current_state_tuple in closed_set:
            continue

        # Get successor states
        successor_states = get_next_nodes(current_node)

        # Add state of node to already searched puzzle states
        closed_set.add(current_state_tuple)
        expanded_nodes += 1

        for successor_state in successor_states:
            successor_node = Node(puzzle_state=successor_state,
                                  parent=current_node,
                                  g_cost=current_node.g_cost + 1,
                                  h_cost=heuristic_function(successor_state))
            heapq.heappush(open_list, successor_node)

    return None, expanded_nodes

# Compare two heuristics on 100 puzzle states
puzzle_nodes_manhattan, puzzle_nodes_hamming = generate_puzzle_nodes(100)
results = {"manhattan": [], "hamming": []}

for name in ["manhattan", "hamming"]:
    print(f"\nRunning A* with {name} heuristic...")
    expanded_counts = []
    start_time = time.time()
    puzzle_number = 1

    if name == "manhattan":
        for puzzle_node in puzzle_nodes_manhattan:
            result = solve_puzzle(puzzle_node, get_heuristic_value_manhattan)
            num_of_expanded_nodes = result[1]
            expanded_counts.append(num_of_expanded_nodes)
            print(f"  Puzzle {puzzle_number} solved ({num_of_expanded_nodes} nodes expanded)")
            puzzle_number += 1
    else:
        for puzzle_node in puzzle_nodes_hamming:
            result = solve_puzzle(puzzle_node, get_heuristic_value_hamming)
            num_of_expanded_nodes = result[1]
            expanded_counts.append(num_of_expanded_nodes)
            print(f"  Puzzle {puzzle_number} solved ({num_of_expanded_nodes} nodes expanded)")
            puzzle_number += 1

    total_time = time.time() - start_time
    mean_expanded = statistics.mean(expanded_counts)
    stdev_expanded = statistics.stdev(expanded_counts)

    results[name] = {
        "mean_nodes": mean_expanded,
        "stdev_nodes": stdev_expanded,
        "total_time": total_time
    }

# Print summary
print("\n=== Comparison Results ===")
print(f"{'Heuristic':<12} {'Mean Nodes':<15} {'StdDev':<10} {'Total Time (s)':<15}")
print("-" * 55)
for key, val in results.items():
    print(f"{key:<12} {val['mean_nodes']:<15.2f} {val['stdev_nodes']:<10.2f} {val['total_time']:<15.2f}")
