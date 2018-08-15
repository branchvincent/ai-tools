import sys; sys.path.append('./astar')

import argparse
from itertools import combinations

from astar import Problem, State

#-------------------------------------------------------------------------------
#   Problem Class
#-------------------------------------------------------------------------------

class MyProblem(Problem):
    '''
    Problem to solve: Superqueens puzzle
    '''

    def __init__(self, board_size=None):
        self.size = board_size
        start_state = MyState([-1]*self.size)
        super(MyProblem, self).__init__(start_state=start_state, goal_state=None)

    def goal_test(self, state):
        '''Tests for the goal state'''
        super(MyProblem, self).goal_test(state)
        return -1 not in state.data

    def heuristic(self, state_a, state_b=None):
        '''Heuristic, the number of attacking queen pairs, to estimate cost to go'''
        super(MyProblem, self).heuristic(state_a, state_b)
        # Get indices for all queens
        a = [(r, c) for r, c in enumerate(state_a.data) if c != -1]

        # Get all queen pairs
        numAttacking = 0
        pairs = list(combinations(a, 2))
        for pair in pairs:
            diff = [abs(q1 - q2) for q1, q2 in zip(*pair)]
            diagAttack = (diff[0] == diff[1])
            knightAttack = (min(diff) == 1 and max(diff) == 2)
            if diagAttack or knightAttack:
                numAttacking += 1
        return numAttacking

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
                final_state = self.solution[-1].state
                f.write('nAttacks = {}\n'.format(self.heuristic(final_state)))
                for row in final_state.board():
                    f.write('\n' + ' '.join(map(str, row)))

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
        # Calculate available rows
        all_cols = range(len(self.data))
        next_col = self.data.index(-1) if -1 in self.data else None
        open_rows = list(set(all_cols) - set(self.data))

        # Calculate neighbors
        if next_col is None:
            return None
        else:
            neighbors = []
            for row in open_rows:
                neighbor = self.data[:]
                neighbor[next_col] = row
                neighbors.append(MyState(neighbor))
            return neighbors

    def cost(self, neighbor):
        '''Cost of a neighboring state'''
        super(MyState, self).cost(neighbor)
        return 0

    def board(self):
        '''Converts state to chess board'''
        n = len(self.data)
        board = [[0]*n for i in range(n)]
        for i, j in enumerate(self.data):
            if j != -1:
                board[j][i] = 1
        return board

#-------------------------------------------------------------------------------
#   Main
#-------------------------------------------------------------------------------

def get_parser():
    parser = argparse.ArgumentParser(description='A* search for superqueens puzzle.')
    parser.add_argument('size', metavar='sz', type=int, help='board size')
    parser.add_argument('-o', '--output_file', default='data/out2.txt', help='file destination of output')
    return parser

def main():
    # Read arguments
    args = get_parser().parse_args()

    # Solve problem
    prob = MyProblem(board_size=args.size)
    prob.solve()
    prob.export(args.output_file)

if __name__ == '__main__':
    main()
