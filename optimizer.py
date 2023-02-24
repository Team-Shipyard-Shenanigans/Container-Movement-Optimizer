from ast import Index
import copy
import time


## Driver function
## Output: Prompts user for input on puzzle type, generates starting state, selects heuristic, then progresses search. Outputs information pertaining to memory and time spent in search
def main():
    p_mode = input("Welcome to my Container Movement Solver! Would you like to continue to try your own? (Y / N) ")
    start = gen_puzzle(p_mode)
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    queuing_function = select_queuing_function(goal)
    t1 = time.time_ns()
    nodes, depth, max_nodes_in_queue, num_nodes_expanded = search(start, goal, queuing_function)
    t2 = time.time_ns()

    print("Queue Depth: %s" % (depth))
    print("Max Queue Size (# Nodes): %s" % (max_nodes_in_queue))
    print("# Nodes Expanded: %s" % (num_nodes_expanded))
    print("Time elapsed: %4.3f s" % ((t2 - t1) / 10**9))


## A* search function
## Parameters: start - matrix representing our 8-puzzle start state
##             goal - matrix representing our 8-puzzle goal state
##             heuristic - a lambda function that describes a heuristic for sorting the node queue
## Output: nodes - the node queue
##         depth - the depth reached by the queue in the search tree
##         num_nodes_expanded - the number of nodes expanded during search
##         max_nodes_in_queue - the maximum number of nodes present in the queue
def search(start, goal, algorithm):
    nodes = [(start, 0)]
    num_nodes_expanded = 0
    max_nodes_in_queue = 1

    while len(nodes) > 0:
        curr = nodes.pop(0)  ## Remove the smallest cost node from the queue
        f_n = algorithm(curr)  ## Calculate cost for displaying
        print("Expanding state with lowest f(n) = %s, g(n) = %s, h(n) = %s \n" % (f_n, curr[1], f_n - curr[1]))
        display_puzzle(curr[0])

        if curr[0] == goal:  ## If our popped node is our goal state, we've solved the puzzle!
            print("Goal State found!")
            return nodes, curr[1], max_nodes_in_queue, num_nodes_expanded  ## return search information to main function for output. Note: g_n = depth of the tree for any node)
        else:
            num_nodes_expanded += 1  ## we expand our popped node, therefore increase number of expanded nodes by 1
            for i in range(0, 12):
                ## Find all valid child states for the following operators
                ##  0 = Move Blank Up, 1 = Move Blank Down, 2 = Move Blank Left, 3 = Move Blank Right
                child_node = get_child(curr[0], i)
                ## Append to queue, ensuring that the g(n) is updated for each node given the previous node.
                if child_node is not None:
                    nodes.append((child_node, curr[1] + 1))

            ## Sort Queue based on our Heuristic
            nodes = sorted(nodes, key=algorithm)

            ## If we have more nodes than our previous maximum in our queue, record new max
            if max_nodes_in_queue <= len(nodes):
                max_nodes_in_queue = len(nodes)


## Helper function to get the child state given preset operators
def get_child(state, operation):
    return state


## Helper function to generate puzzle
## Parameters: string p_mode
## Output: if p_mode equals "Y", prompt user to generate own puzzle, else prompt them to choose desired default puzzle by difficulty.
def gen_puzzle(p_mode="N"):
    puzzle = []
    if p_mode == "Y":
        puzzle = [["?", "?", "?"], ["?", "?", "?"], ["?", "?", "?"]]

        print("Please only enter numbers from 0-8, do not reuse numbers.")

        for i in range(0, 9):
            puzzle[int(i / 3)][i % 3] = int(input("%s\n%s\n%s\nNumber? " % (puzzle[0], puzzle[1], puzzle[2])))
    else:
        p_difficulty = int(input("Please enter your desired default puzzle difficulty level! \n 0 - Trivial through 7 - Very Difficult \n"))
        ## examples taken from Dr. Keogh's lecture slides
        if p_difficulty == 0:
            puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        elif p_difficulty == 1:
            puzzle = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
        elif p_difficulty == 2:
            puzzle = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
        elif p_difficulty == 3:
            puzzle = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
        elif p_difficulty == 4:
            puzzle = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
        elif p_difficulty == 5:
            puzzle = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
        elif p_difficulty == 6:
            puzzle = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
        elif p_difficulty == 7:
            puzzle = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]

    display_puzzle(puzzle)
    return puzzle


## Helper function for selecting queuing function (the heuristic)
## Parameters: goal state
## Output: Lambda expression for calculating heuristic based on inputted state.
def select_queuing_function(goal):
    algo = int(input("Select a search heuristic: 0 - Uniform Cost \n 1 - Misplaced Tile \n 2 - Manhattan Distance\n"))
    if algo == 0:
        return lambda i: i[1]
    elif algo == 1:
        return lambda i: i[1] + get_misplaced_tiles(i[0], goal)
    elif algo == 2:
        return lambda i: i[1] + get_manhattan(i[0], goal)


## Parameters: two matrices representing the current state and the goal state of the 8-puzzle matrix
## Output: The sum of Manhattan distances of all misplaced tiles
def get_manhattan(state, goal):
    distance = 0

    ## We know the goal state is when we have 1 - 3 in the first row, 4 - 6 in the second row, and 7-8, 0 in the third row.
    # That means the following correspondance to indices can be made
    # 1 = (0, 0), 2 = (0, 1), 3 = (0, 2), 4 = (1, 0), 5 = (1, 1), 6 = (1, 2), 7 = (2, 0), 8 = (2, 1), 0 = (2, 2)
    # The Manhattan Distance between any two indices is defined as |i_2 - i_1| + |j_2 - j_1|
    # We want to find the sum of the manhattan distances of all misplaced tiles.

    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] != goal[i][j]:
                goal_indices = index_mapper(state[i][j])
                distance += abs(i - goal_indices[0]) + abs(j - goal_indices[1])
    return distance


## Parameters: an integer
## Output: The indices of the position of the integer in the goal state of the 8-puzzle matrix.
def index_mapper(value):
    ## shift values over so 1 -> 0, 2 -> 1, ... 0 -> 8
    value = (value - 1) % 9
    ## use earlier algorithm to convert values of range(0, 9) to appropriate index in 2d list
    ## ex 8 / 3 = 2, 8 % 3 = 2 -> (2, 2)
    return (int(value / 3), value % 3)


## Parameters: two matrices representing the current state and the goal state of the 8-puzzle matrix
## Output: The number of tiles such that state[i][j] != goal[i][j]
def get_misplaced_tiles(state, goal):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] != goal[i][j]:
                count += 1
    return count


## Helper function to display puzzle
## Output: Displays 3 by 3 matrix
def display_puzzle(puzzle):
    print("%s\n%s\n%s" % (puzzle[0], puzzle[1], puzzle[2]))


main()
