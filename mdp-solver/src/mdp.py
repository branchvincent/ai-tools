from copy import deepcopy
import numpy as np

def argmax(xs, fn):
    fs = map(fn, xs)
    i = np.argmax(fs)
    return xs[i], fs[i]

class MDP:
    def __init__(self, rewards, transitions, delta):
        # Set reward and transition
        self.rewards = rewards
        self.transitions = transitions
        self.delta = delta
        # Deduce states
        self.states = set(rewards.keys())

    def A(self, state):
        '''Actions'''
        return self.rewards[state].keys()

    def R(self, state, action):
        '''Reward'''
        return self.rewards[state][action]

    def P(self, state, action):
        '''Transitional probabilities'''
        return self.transitions[state][action]

    def value_iter(self, eps=1e-5):
        '''Solve by value iteration'''
        pi, V = {}, {s: 0 for s in self.states}
        delta = float('inf')
        # Iterate until values converge
        while delta >= eps * (1 - self.delta) / self.delta:
            VV, delta = V.copy(), 0
            # Calculate optimal action at each state
            for s in self.states:
                pi[s], V[s] = argmax(self.A(s), lambda a: self.bellman(s, a, VV))
                delta = max(delta, abs(V[s] - VV[s]))
        return pi, V

    def policy_iter(self, pi):
        '''Solve by policy iteration'''
        V = {s: 0 for s in self.states}
        solved = False
        # Iterate until policy converges
        while not solved:
            solved = True
            V = self.policy_eval(pi, V)
            # Calculate optimal action at each state
            for s in self.states:
                a, _ = argmax(self.A(s), lambda a: self.bellman(s, a, V))
                # Update action
                if pi[s] != a:
                    pi[s] = a
                    solved = False
        return pi, V

    def policy_eval(self, pi, V, N=25):
        '''Evaluate policy using N-step horizon'''
        for _ in range(N):
            for s in self.states:
                V[s] = self.bellman(s, pi[s], V)
        return V

    def exp_util(self, s, a, V):
        '''Expected utility'''
        util = [p * V[ss] for ss, p in self.P(s, a).iteritems()]
        return sum(util)

    def bellman(self, s, a, V):
        '''Bellman equation'''
        return self.R(s, a) + self.delta * self.exp_util(s, a, V)

def main():
    # Solver function
    def solve(mdp, complete=False):
        # Compute value iteration
        pi, V = mdp.value_iter()
        if complete:
            print 'Value iter\n\tpi = {}\n\t V = {}'.format(pi, V)
            # Compute policy iteration
            pi0 = {s: 'idle' for s in mdp.states}
            pi, V = mdp.policy_iter(pi0)
            print 'Policy iter\n\tpi = {}\n\t V = {}'.format(pi, V)
        else:
            print pi

    # Initialize MDP
    rewards = {
        'top': {'drive': 2, 'idle': 3},
        'rolling': {'drive': 0, 'idle': 1},
        'bottom': {'drive': 0, 'idle': 1}
    }
    transitions = {
        'top': {
            'drive': {'top': 0.9, 'rolling': 0.1},
            'idle': {'top': 0.7, 'rolling': 0.3}
        },
        'rolling': {
            'drive': {'top': 0.3, 'rolling': 0.6, 'bottom': 0.1},
            'idle': {'bottom': 1}
        },
        'bottom': {
            'drive': {'top': 0.6, 'bottom': 0.4},
            'idle': {'bottom': 1}
        }
    }
    delta = 0.8

    # Solve original problem
    print 'ORIGINAL'
    mdp = MDP(rewards, transitions, delta)
    solve(mdp, True)
    # Modify delta
    print '\nNEW DISCOUNT'
    mdp1 = deepcopy(mdp)
    mdp1.delta = 0.5
    solve(mdp1)
    # Modify transition
    print '\nNEW TRANSITION'
    mdp2 = deepcopy(mdp)
    mdp2.transitions['bottom']['drive'] = {'top': 0.1, 'rolling': 0.9}
    solve(mdp2)
    # Modify reward
    print '\nNEW REWARD'
    mdp3 = deepcopy(mdp)
    mdp3.rewards['bottom']['idle'] = 3
    solve(mdp3)

if __name__ == '__main__':
    main()
