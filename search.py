# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited = set() # store state
    dfs_stack = util.Stack()  # stores (state, direction, cost)
    start_state = problem.getStartState()
    initial = (problem.getStartState(), 'Nothing', 0)
    dfs_stack.push(initial)
    actions = [] # stores the tuple (state, dir, cost)
    # act_stack = util.Stack() # stores actions
    count = 0

    while not dfs_stack.isEmpty():
        current_tuple = dfs_stack.pop()
        # print current_tuple
        current_state = current_tuple[0]
        # print 'current state[1]: ', current_state
        # print 'current direction[2]', current_tuple[1]

        if current_state in visited:
            continue

        if not count == 0:
            actions.append(current_tuple)

        visited.add(current_state)

        if problem.isGoalState(current_state):
            # print 'find it!'
            res = []
            for action in actions:
                res.append(action[1])
            # util.manhattanDistance(state)
            return res
        else:
            dead_end = True
            successors = problem.getSuccessors(current_state)  # list of tuple
            for x in successors:
                if x[0] not in visited:
                    dead_end = False
                dfs_stack.push(x)

        if dead_end:
            actions.pop()
            while True:
                if not len(actions) == 0:
                    action = actions[-1]
                    neighbours = problem.getSuccessors(action[0])
                else:
                    neighbours = problem.getSuccessors(start_state)

                has_other_branch = False
                for neighbour in neighbours:
                    if neighbour[0] not in visited:
                        has_other_branch = True

                if not has_other_branch:
                    actions.pop()
                    # print 'popped this node'
                else:
                    # print 'starting a new branch'
                    break
        count += 1

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    start_state = problem.getStartState()
    visited = [start_state]
    actions = []
    bfs_queue = util.Queue()
    initial_tuple = (start_state, actions, visited)  # a tuple of state, action and visited set

    bfs_queue.push(initial_tuple)
    global_visited = []
    while not bfs_queue.isEmpty():
        current_tuple = bfs_queue.pop()
        # print 'current tup', current_tuple
        current_state = current_tuple[0]
        if current_state in global_visited:
            continue

        global_visited.append(current_state)
        # print 'current state', current_state
        current_action = current_tuple[1]
        # print 'current act: ', current_action
        current_visited = current_tuple[2]
        # print 'current visited: ', current_visited

        if problem.isGoalState(current_state):
            # print 'find it'
            return current_action
        else:
            successors = problem.getSuccessors(current_state)
            for suc in successors:
                if suc[0] not in current_visited:
                    updated_act = current_action + [suc[1]]
                    # print 'u_act: ', updated_act
                    updated_visited = current_visited + [suc[0]]
                    updated_tuple = (suc[0], updated_act, updated_visited)
                    # print 'u_tuple: ', updated_tuple
                    bfs_queue.push(updated_tuple)
        # print ''

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited = []
    actions = []
    cost = 0
    pri_queue = util.PriorityQueue()
    initial = ((start_state, actions), cost)
    print 'initial: ', initial

    pri_queue.push(initial)

    while not pri_queue.isEmpty():
        current_tuple = pri_queue.pop()
        current_state = current_tuple[0][0]
        current_actions = current_tuple[0][1]
        current_cost = current_tuple[1]

        if current_state in visited:
            continue

        if problem.isGoalState(current_state):
            return current_actions
        else:
            successors = problem.getSuccessors(current_state)  # tuple
            for suc in successors:
                pri_queue.update(((suc[0], current_state + [suc[1]]), current_cost + suc[2]))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
