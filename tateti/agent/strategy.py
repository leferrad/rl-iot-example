# -*- coding: utf-8 -*-

"""Strategies for exploration-exploitation of Agents"""

__author__ = 'leferrad'

# More info about strategies:
# - https://bit.ly/2ITtWh2
# - https://sudeepraja.github.io/Bandits/
# - https://mpatacchiola.github.io/blog/2017/08/14/dissecting-reinforcement-learning-6.html

import numpy as np


class Strategy(object):
    def __init__(self, exploit_func, seed=123):
        self.exploit_func = exploit_func
        self.seed = seed
        np.random.seed(seed)

    def sample_action(self, v):
        pass

    def update(self):
        pass


class EpsilonGreedy(Strategy):
    """Epsilon Greedy (a.k.a ε-greedy) strategy"""
    def __init__(self, exploit_func, epsilon=0.95, decay=0.95, epsilon_min=0.1, seed=123):
        self.epsilon_init = epsilon
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decay = decay

        Strategy.__init__(self, exploit_func=exploit_func, seed=seed)

    def sample_action(self, v, explore=True):
        # Assuming as many actions as number of elements in v
        if explore and np.random.uniform(0, 1) > self.epsilon:
            a_int = np.random.choice(range(len(v)))
        else:
            a_int = self.exploit_func(v)

        return a_int

    def update(self):
        self.epsilon *= self.decay
        self.epsilon = max(self.epsilon, self.epsilon_min)

    def reset(self):
        self.epsilon = self.epsilon_init


class Boltzmann(Strategy):
    # TODO: not having deterministic results

    def __init__(self, exploit_func, epsilon=0.9, decay=0.95, epsilon_min=0.05, seed=123):
        self.epsilon_init = epsilon
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decay = decay

        Strategy.__init__(self, exploit_func=exploit_func, seed=seed)

    def update(self):
        self.epsilon *= self.decay
        self.epsilon = max(self.epsilon, self.epsilon_min)

    def reset(self):
        self.epsilon = self.epsilon_init

    @staticmethod
    def get_boltzmann_values(p):
        max_p = np.max(p)
        exp_p = [np.exp((p_i - max_p)) for p_i in p]
        sum_exp_p = np.sum(exp_p)
        softmax_p = [exp_p_i / sum_exp_p for exp_p_i in exp_p]

        # Fix to have positive values (round error)
        softmax_p = [np.max((s, 1e-10)) for s in softmax_p]

        # Fix to sum 1 (round error)
        delta = (1.0 - np.sum(softmax_p)) / len(softmax_p)
        softmax_p = [s + delta for s in softmax_p]

        return softmax_p

    def sample_action(self, v, explore=True):
        # Assuming as many actions as number of elements in v
        if explore and np.random.uniform(0, 1) > self.epsilon:
            # Explore through Boltzmann method
            probability_actions = self.get_boltzmann_values(v)
            a_int = np.random.choice(range(len(v)), p=probability_actions)
        else:
            a_int = self.exploit_func(v)

        return a_int
