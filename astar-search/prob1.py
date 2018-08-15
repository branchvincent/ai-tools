import sys; sys.path.append('./astar')

import argparse
import numpy as np
from itertools import product

from astar import Problem, State

#-------------------------------------------------------------------------------
#   Problem Class
#-------------------------------------------------------------------------------

class MyProblem(Problem):
    '''
    Problem to solve: Knights puzzle
    '''

    def __init__(self, start_state=None, goal_state=None, heuristic_helper=None):
        super(MyProblem, self).__init__(start_state=start_state, goal_state=goal_state)
        self.heuristic_helper = heuristic_helper

    def goal_test(self, state):
        '''Tests for the goal state'''
        super(MyProblem, self).goal_test(state)
        return np.all(state.data == self.goal_state.data)

    def heuristic(self, state_a, state_b):
        '''Heuristic, the summed minimum knight moves, to estimate cost to go'''
        super(MyProblem, self).heuristic(state_a, state_b)
        cost = 0
        for i, a, in enumerate(state_a.data.flatten()):
            if a != 0:
                j = list(state_b.data.flatten()).index(a)
                cost += self.heuristic_helper[16*i + j]
        return cost

    def solve(self):
        '''Solves the search problem'''
        super(MyProblem, self).solve()

    def export(self, filename):
        '''Exports solution to a file'''
        super(MyProblem, self).export()
        with open(filename, 'w') as f:
            if self.solution is None:
                f.write('WARNING: No solution found')
            else:
                f.write('length = {}\n'.format(len(self.solution) - 1))
                for node in self.solution:
                    np.savetxt(f, node.state.data, fmt='%i', header=' ', comments='')

#-------------------------------------------------------------------------------
#   State Class
#-------------------------------------------------------------------------------

class MyState(State):
    '''
    State of the problem: 2D chess board
    '''

    def __init__(self, data):
        super(MyState, self).__init__()
        self.data = data

    def neighbors(self):
        '''Neighboring states'''
        super(MyState, self).neighbors()
        # Calculate all moves
        nr, nc = self.data.shape
        in_bounds = lambda (i, j): 0 <= i < nr and 0 <= j < nc
        r0, c0 = zip(*np.where(self.data == 0))[0]
        relative_moves = list(product((1, -1), (2, -2))) + list(product((2, -2), (1, -1)))
        moves = filter(in_bounds, [(r0 + i, c0 + j) for i, j in relative_moves])

        # Calculate all neighbors
        neighbors = []
        for move in moves:
            neighbor = np.copy(self.data)
            neighbor[move] = 0
            neighbor[r0,c0] = self.data[move]
            neighbors.append(MyState(neighbor))
        return neighbors

    def cost(self, neighbor):
        '''Cost of a neighboring state'''
        super(MyState, self).cost(neighbor)
        return 1

#-------------------------------------------------------------------------------
#   Main
#-------------------------------------------------------------------------------

def get_parser():
    parser = argparse.ArgumentParser(description='A* search for knights puzzle.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', metavar='f', help='file containing initial state')
    parser.add_argument('-hr', '--heuristic_file', default='data/heur1.txt', help='file containing heuristic helper')
    parser.add_argument('-o', '--output_file', default='data/out1.txt', help='file destination of output')
    return parser

def main():
    # Read arguments
    args = get_parser().parse_args()

    # Read initial state
    start_data = np.loadtxt(args.file, dtype=int)
    start_state = MyState(start_data)

    # Setup problem
    goal_data = np.asarray(range(1, 16) + [0]).reshape(4,4)
    goal_state = MyState(goal_data)

    with open(args.heuristic_file) as f:
        heuristic_helper = map(int, f.read().split())

    # Solve problem
    prob = MyProblem(start_state=start_state, goal_state=goal_state, heuristic_helper=heuristic_helper)
    prob.solve()
    prob.export(args.output_file)

if __name__ == '__main__':
    main()
