from abc import ABCMeta, abstractmethod
from Queue import PriorityQueue

# Constants

INFINITY = float('inf')

#-------------------------------------------------------------------------------
#   Problem Class (Abstract)
#-------------------------------------------------------------------------------

class Problem(object):
    '''
    Problem to solve
    '''
    __metaclass__ = ABCMeta

    def __init__(self, start_state=None, goal_state=None):
        self.start_state = start_state
        self.goal_state = goal_state
        self.solution = None
        self.astar = AStar()

    @abstractmethod
    def goal_test(self, state):
        '''Tests for the goal state'''
        pass

    @abstractmethod
    def heuristic(self, state_a, state_b):
        '''Heuristic to estimate cost to go'''
        pass

    def solve(self):
        '''Solves the search problem'''
        self.solution = self.astar.search(start=self.start_state,
                                          goal=self.goal_state,
                                          heuristic=self.heuristic,
                                          goal_test=self.goal_test)

    def export(self):
        '''Exports solution to a file'''
        pass

#-------------------------------------------------------------------------------
#   State Class (Abstract)
#-------------------------------------------------------------------------------

class State(object):
    '''
    State of the problem
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def neighbors(self):
        '''Neighboring states'''
        pass

    @abstractmethod
    def cost(self, neighbor):
        '''Cost of a neighboring state'''
        pass

#-------------------------------------------------------------------------------
#   Node Class
#-------------------------------------------------------------------------------

class Node(object):
    '''
    Search node in the tree
    '''

    def __init__(self, state=None, parent=None, g=INFINITY, h=INFINITY):
        self.state = state
        self.parent = parent
        self.g = g   # cost incurred (actual)
        self.h = h   # cost to go (heuristic)

    def __cmp__(self, node):
        return cmp(self.f(), node.f())

    def f(self):
        '''Total estimated path cost'''
        return self.g + self.h

#-------------------------------------------------------------------------------
#   AStar Class
#-------------------------------------------------------------------------------

class AStar(object):
    '''
    Search algorithm
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        self.explored = set()

    def search(self, start, goal, heuristic, goal_test):
        '''Searches for the optimal path'''
        self.reset()

        # Initialize frontier with start node
        node = Node(state=start, parent=None, g=0, h=heuristic(start, goal))
        frontier = PriorityQueue()
        frontier.put(node)

        # Explore all frontier nodes
        while not frontier.empty():
            # Get node with lowest total cost
            node = frontier.get()

            # Return, if goal state
            if goal_test(node.state):
                return self.get_path(node)

            # Add state to explored
            self.explored.add(node.state)

            # Search each child state
            for child_state in node.state.neighbors():
                child_g = node.g + node.state.cost(child_state)
                child_h = heuristic(child_state, goal)
                child = Node(state=child_state, parent=node, g=child_g, h=child_h)
                if child.state not in self.explored:# or child.f() < node.f():
                    frontier.put(child)
        return None

    def get_path(self, node):
        '''Get path from start state to goal state'''
        path = [node]
        while node.parent is not None:
            node = node.parent
            path.append(node)
        return list(reversed(path))

    def get_depth(self):
        '''Get depth of search tree'''
        return len(self.explored)
