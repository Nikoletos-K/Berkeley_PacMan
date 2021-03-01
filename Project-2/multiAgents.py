# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        from util import  manhattanDistance

        foodList = newFood.asList()
        ghostList = successorGameState.getGhostPositions()
        distancesList = []

        # --------------- Food factor --------------------
        # Checking every food distance from pacman
        for food in foodList:
            food_from_pacman = manhattanDistance(newPos,food)
            distancesList.append(food_from_pacman)

        if len(distancesList) == 0 :
            # if no food left ,don't go from there so value =  -1
            min_foodDistance = -1
        else:
            # return the minimun of this list
            min_foodDistance = min(distancesList)

        # food factor as a posibility
        foodFactor = 1 / float(min_foodDistance)

        # --------------- Ghost factor -----------------
        ghostDistances = 0
        for ghost in ghostList:
            ghost_from_pacman =  manhattanDistance(newPos,ghost)
            # if ghost very close , return -inf to go on another direction
            if(ghost_from_pacman <= 1):
                return float("-inf")
            # sum distance of pacman - ghosts
            ghostDistances =+  ghost_from_pacman

        if ghostDistances == 0 :
            ghostFactor = 0
        else:
            # ghost factor = 1/sum_of_ghostDistances
            ghostFactor = 1 / float(ghostDistances)

        return successorGameState.getScore() + foodFactor - ghostFactor

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # minValue and maxValue returns a tuple ( action , min / max )

        # Function same as MINIMAX-DECISION in the AI book ( 2nd edition , page 210)
        agent = 0
        depth = 0

        # Initial state
        return self.maxValue(gameState,agent,depth)[0]

    # function that checks if the game has come to a terminal state
    def TerminalTest(self,gameState,depth):
        # self.depth is data member of this agent and it is the max depth
        if depth == self.depth*gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return True

        return False

    # minimax function returns value
    def minimax(self,gameState,agent,depth):

        # tree possible situations:

        # checking if we are in a terminal state in order to return the evaluation value
        if self.TerminalTest(gameState,depth):
            return self.evaluationFunction(gameState)


        if agent == 0:
            # case index is pacman (MIN) , maximize
            return self.maxValue(gameState,agent,depth)[1]
        else:
            # case it is a ghost (MAX) , minimize
            return  self.minValue(gameState,agent,depth)[1]

    def minValue(self,gameState,agent,depth):

        # initialazation of optimal function with -infinitum
        optimalAction = (None,float("inf"))
        # increase depth,agent

        # loop for every action in legal actions
        for action in gameState.getLegalActions(agent):
            # Returns the successor game state after an agent takes an action
            succesorGameState = gameState.generateSuccessor(agent,action)
            newDepth = depth + 1
            newAgent = newDepth % gameState.getNumAgents()

            # new agent will be in the bigger depth , mod is used because as the depth increase , agent index increase (if mod == 0 then agent is pacman) and
            v = self.minimax(succesorGameState,newAgent,newDepth)
            succesorAction = (action,v)

            # if successorAction minimax value is smaller than the optimal exchange
            if succesorAction[1] < optimalAction[1] :
                optimalAction = succesorAction


        return optimalAction

    def maxValue(self,gameState,agent,depth):

        # same as minValue with -infinitum initialaization

        optimalAction = (None,float("-inf"))
        for action in gameState.getLegalActions(agent):
            succesorGameState = gameState.generateSuccessor(agent,action)
            # Returns the successor game state after an agent takes an action
            newDepth = depth + 1
            newAgent = newDepth % gameState.getNumAgents()

            v = self.minimax(succesorGameState,newAgent,newDepth)
            succesorAction = (action,v)

            # if successorAction minimax value is bigger than the optimal exchange
            if succesorAction[1] > optimalAction[1] :
                optimalAction = succesorAction


        return optimalAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
         # minValue and maxValue returns a tuple ( action , min / max )

        # Function same as MINIMAX-DECISION in the AI book ( 2nd edition , page 210)
        agent = 0
        depth = 0
        v = self.maxValue(gameState,agent,depth,float("-inf"),float("inf"))[0]
        # Initial state

        return v

    def TerminalTest(self,gameState,depth):

        if depth == self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return True

        return False

    def alphabeta(self,gameState,agent,depth,a,b):

        # same as minimax

        if self.TerminalTest(gameState,depth):
            return self.evaluationFunction(gameState)


        if agent == 0:
            # case index is pacman (MIN) , maximize
            return self.maxValue(gameState,agent,depth,a,b)[1]
        else:
            # case it is a ghost (MAX) , minimize
            return  self.minValue(gameState,agent,depth,a,b)[1]

    def maxValue(self,gameState,agent,depth,a,b):

        # same as minValue with -infinitum initialaization

        optimalAction = (None,float("-inf"))
        for action in gameState.getLegalActions(agent):

            succesorGameState = gameState.generateSuccessor(agent,action)
            # Returns the successor game state after an agent takes an action
            newDepth = depth + 1
            newAgent = newDepth % gameState.getNumAgents()
            v = self.alphabeta(succesorGameState,newAgent,newDepth,a,b)
            succesorAction = (action, v)

            # if successorAction minimax value is bigger than the optimal exchange
            if succesorAction[1] > optimalAction[1] :
                optimalAction = succesorAction

            # if current value is bigger than b then cut off
            if optimalAction[1] > b :
                return optimalAction

            # else inform a if this value is bigger than a
            a = max(a,optimalAction[1])

        return optimalAction

    def minValue(self,gameState,agent,depth,a,b):

        # same as minValue with -infinitum initialaization

        optimalAction = (None,float("inf"))
        for action in gameState.getLegalActions(agent):

            succesorGameState = gameState.generateSuccessor(agent,action)
            # Returns the successor game state after an agent takes an action
            newDepth = depth + 1
            newAgent = newDepth % gameState.getNumAgents()
            v = self.alphabeta(succesorGameState,newAgent,newDepth,a,b)
            succesorAction = (action, v)

            # if successorAction minimax value is bigger than the optimal exchange
            if succesorAction[1] < optimalAction[1] :
                optimalAction = succesorAction

            # if current value is smaller than a then cut off
            if optimalAction[1] < a :
                return optimalAction

            # else inform b with the minimun of value or b
            b = min(b,optimalAction[1])

        return optimalAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # I initialize agent with self.index (index is data member of this agent)
        agent = self.index
        depth = 0
        action = self.maxValue(gameState,agent,depth)[0]
        return action

    def TerminalTest(self,gameState,depth):

        # checking until the max depth
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return True

        return False

    def expectiminimax(self,gameState,agent,depth):

        # if depth is max depth and agent% gameState.getNumAgents() ==0 ,means that we reach the end
        if self.TerminalTest(gameState,depth) and agent% gameState.getNumAgents() ==0:
            return None, self.evaluationFunction(gameState)

        if agent  == 0:
            # case pacman
            return self.maxValue(gameState,agent,depth)
        else:
            # case of ghosts
            return self.expValue(gameState,agent,depth)

    def maxValue(self,gameState,agent,depth):


        # checking for legal actions in this node,if not return evaluation function
        if len(gameState.getLegalActions(agent)) == 0:
            return None,self.evaluationFunction(gameState)

        # same as before
        optimalAction = (None,float("-inf"))
        newAgent = (agent+1) % gameState.getNumAgents()
        newDepth = depth+1

        for action in gameState.getLegalActions(agent):
            succesorGameState = gameState.generateSuccessor(agent,action)
            a,v = self.expectiminimax(succesorGameState,newAgent,newDepth)
            succesor = (action,v)

            # if successorAction minimax value is bigger than the optimal exchange
            if v > optimalAction[1] :
                optimalAction = succesor

        return optimalAction

    def expValue(self,gameState,agent,depth):

        totalValue=0
        newAgent = (agent+1) % gameState.getNumAgents()

        if len(gameState.getLegalActions(agent)) == 0 :
            return None,self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agent):
            succesorGameState = gameState.generateSuccessor(agent,action)
            a,v = self.expectiminimax(succesorGameState,newAgent,depth)
            totalValue = totalValue + v

        # total value is the sum of the values of children nodes
        # average is that sum / the number of children (as in theory)
        averageValue = float(totalValue) / float(len(gameState.getLegalActions(agent)))

        return  None,averageValue


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos =  currentGameState.getPacmanPosition()
    newFood =  currentGameState.getFood()
    newGhostStates =  currentGameState.getGhostStates()
    # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    # same as question 1
    from util import  manhattanDistance

    foodList = newFood.asList()
    ghostList = currentGameState.getGhostPositions()
    distancesList = []


    for food in foodList:
        food_from_pacman = manhattanDistance(newPos,food)
        distancesList.append(food_from_pacman)


    if len(distancesList) == 0 :
        min_foodDistance = -1
    else:
        min_foodDistance = min(distancesList)

    foodFactor = 1.0 / float(min_foodDistance)

    ghostDistances = 0

    for ghost in ghostList:
        ghostList =  currentGameState.getGhostPositions()
        ghost_from_pacman =  manhattanDistance(newPos,ghost)
        if(ghost_from_pacman <= 1):
            return float("-inf")
        ghostDistances =+  ghost_from_pacman

    if ghostDistances == 0 :
        ghostFactor = -1.0
    else:
        ghostFactor = 1.0 / float(ghostDistances)

    # the only difference is that numOfCapsules is also a factor , moving pacman to eat those capsules
    newCapsule = currentGameState.getCapsules()
    numberOfCapsules = len(newCapsule)

    return currentGameState.getScore() + foodFactor - ghostFactor - numberOfCapsules

# Abbreviation
better = betterEvaluationFunction

