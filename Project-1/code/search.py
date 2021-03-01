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

    # Node is a tuple : (state,action,cost)
    from util import Stack


    startState = problem.getStartState()    # Initial position

    actions = [] # Actions is the list I

    if problem.isGoalState(startState):
        return actions

    frontier = Stack()  # Dfs implementation with a stack
    frontier.push((startState,actions)) # Insert to stack first element: tuple (startState(x,y) ,list Of Actions[])
    explored = set() # Python set , a data structure implemented with hash table,giving us big-O(1) complexity

    while not frontier.isEmpty():       # While we have tuples inside stack

        node = frontier.pop()   # Pop the first one
        state = node[0]     # state = (x,y)
        path = node[1]      # list of actions for this state

        if state not in explored:

            explored.add(state)     # State insert to set , in order not to visit it again

            if problem.isGoalState(state):  # If we reach the wanted state , end the algorithm and return the path for this state
                return path

            successors = problem.getSuccessors(state)   # Successors are nodes children , the state that node is connected

            for child in successors:        # For every child , push it's new path to the stack

                if child not in explored:
                    informedPath = path + [child[1]]        # New path is the actions untill this clild + the actions of this clild
                    frontier.push((child[0],informedPath))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # Bfs is the same with dfs , but implemented with a Queue(FIFO) and not with a stack
    from util import Queue

    startState = problem.getStartState()
    actions = []

    if problem.isGoalState(startState):
        return actions

    frontier = Queue()
    frontier.push((startState,actions))
    explored = set()

    while not frontier.isEmpty():

        node = frontier.pop()
        state = node[0]
        path = node[1]

        if state not in explored:

            explored.add(state)

            if problem.isGoalState(state):
                return path

            successors = problem.getSuccessors(state)

            for child in successors:

                if child not in explored:
                    informedPath = path + [child[1]]
                    frontier.push((child[0],informedPath))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # UniformCostSearch is the same with dfs,bfs , but implemented with a PriorityQueue and not with a stack or Queue
    # Priority in this queue it is the cost
    # Bigger Cost -> Smaller Priority , because it is implemented using increasing sort, and every time we pop the first element

    from util import PriorityQueue

    startState = problem.getStartState()
    actions = []
    
    if problem.isGoalState(startState):
        return actions

    frontier = PriorityQueue()
    startStateCost = problem.getCostOfActions(actions)  # Start cost will be equal to zero
    frontier.push((startState,actions),startStateCost)
    explored = set()

    while not frontier.isEmpty():

        node = frontier.pop()
        state = node[0]
        path = node[1]

        if state not in explored:

            explored.add(state)

            if problem.isGoalState(state):
                return path

            successors = problem.getSuccessors(state)

            for child in successors:

                if child not in explored:

                    newPath = path + [child[1]]
                    # We make the new list of actions and then we calculate the cost , using the provided function
                    newPathCost = problem.getCostOfActions(newPath)

                    frontier.update((child[0],newPath),newPathCost)
                    # I am using update ,in order to have a rearrange in case of same path with smaller cost



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

    # Implementation similar to the above
    # The only change is that priority of the queue isn't only the cost
    # but the cost plus the result of the heuristic function

    from util import PriorityQueue


    startState = problem.getStartState()
    actions = []

    if problem.isGoalState(startState):
        return actions

    frontier = PriorityQueue()
    startStateCost = problem.getCostOfActions(actions)
    frontier.push((startState,actions),startStateCost)
    explored = set()

    while not frontier.isEmpty():

        node = frontier.pop()
        state = node[0]
        path = node[1]

        if state not in explored:

            explored.add(state)

            if problem.isGoalState(state):
                return path

            successors = problem.getSuccessors(state)

            for child in successors:

                if child not in explored:

                    newPath = path + [child[1]]
                    newPathCost = problem.getCostOfActions(newPath)

                    # Priority = Cost + ResultOfHeuristic
                    frontier.update((child[0],newPath),(newPathCost+heuristic(child[0],problem)))



    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
