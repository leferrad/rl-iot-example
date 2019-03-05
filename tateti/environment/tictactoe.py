# -*- coding: utf-8 -*-

"""Model of the environment that will be used for every agent"""

# NOTE: highly based on https://github.com/lazyprogrammer/machine_learning_examples/blob/master/rl/tic_tac_toe.py

__author__ = 'leferrad'

import numpy as np
import itertools
import copy


def standard_reward(env, sym, reward_positive=1, reward_negative=0):
    reward = reward_negative
    if env.game_over():
        reward = reward_positive if env.winner == sym else reward_negative
    return reward


# TODO: try other reward functions and check what happens!

available_rewards = {'standard': standard_reward}


def integer_phi(env):
    # returns the current state, represented as an int
    # from 0...|S|-1, where S = set of all possible states
    # |S| = 3^(BOARD SIZE), since each cell can have 3 possible values - empty, x, o
    # some states are not possible, e.g. all cells are x, but we ignore that detail
    # this is like finding the integer represented by a base-3 number

    v_mapping = {Environment.SYMBOL_EMPTY: 0, Environment.SYMBOL_X: 1, Environment.SYMBOL_O: 2}
    k = 0
    h = 0

    for i in range(Environment.BOARD_LENGTH):
        for j in range(Environment.BOARD_LENGTH):
            v = v_mapping[env.board[i, j]]
            h += (3 ** k) * v
            k += 1
    return h


# TODO: try other phi functions and check what happens!

available_phis = {"integer": integer_phi}


class Environment(object):
    BOARD_LENGTH = 3  # TODO: parameter of Environment?
    SYMBOL_X = -1
    SYMBOL_O = 1
    SYMBOL_EMPTY = 0

    available_actions = list(itertools.product(range(BOARD_LENGTH), range(BOARD_LENGTH)))
    n_actions = len(available_actions)

    cell_repr = {SYMBOL_X: " x ", SYMBOL_O: " o ", SYMBOL_EMPTY: "   "}

    def __init__(self, reward_function='standard', phi_function="integer", seed=123):
        self.board = np.zeros((Environment.BOARD_LENGTH, Environment.BOARD_LENGTH))

        self.winner = None
        self.ended = False
        self.num_states = 3 ** (Environment.BOARD_LENGTH * Environment.BOARD_LENGTH)
        
        self.actions_taken = []

        assert reward_function in available_rewards
        self.reward_function = lambda sym: available_rewards[reward_function](self, sym)
        assert phi_function in available_phis
        self.phi_function = lambda: available_phis[phi_function](self)

        self.seed = seed
        np.random.seed(seed)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def is_draw(self):
        return self.ended and self.winner is None

    def get_env_string(self):
        # cell_repr maps cell elements to 'x', 'o' or ' '
        cell_repr = {k: v.strip() if len(v.strip()) != 0 else " " for (k, v) in self.cell_repr.items()}

        return "".join([cell_repr[int(x)] for x in np.nditer(self.board)])

    def get_possible_moves(self):
        return [(i, j) for (i, j) in self.available_actions if self.is_empty(i, j)]

    @staticmethod
    def get_possible_moves_from_str(env_str):
        return list(map(lambda x_a: x_a[1],  # Get corresponding action
                        filter(lambda x_a: x_a[0] == " ",  # Get only empty cells
                               # x_a: tuple of (element of cell, action)
                               zip(env_str, Environment.available_actions))))

    def game_over(self, force_recalculate=True):
        # returns true if game over (a player has won or it's a draw)
        # otherwise returns false
        # also sets 'winner' instance variable and 'ended' instance variable
        if not force_recalculate and self.ended:
            return self.ended

        # check rows
        for i in range(Environment.BOARD_LENGTH):
            for player in (self.SYMBOL_X, self.SYMBOL_O):
                if self.board[i].sum() == player * Environment.BOARD_LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # check columns
        for j in range(Environment.BOARD_LENGTH):
            for player in (self.SYMBOL_X, self.SYMBOL_O):
                if self.board[:, j].sum() == player * Environment.BOARD_LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # check diagonals
        for player in (self.SYMBOL_X, self.SYMBOL_O):
            # top-left -> bottom-right diagonal
            if self.board.trace() == player * Environment.BOARD_LENGTH:
                self.winner = player
                self.ended = True
                return True
            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player * Environment.BOARD_LENGTH:
                self.winner = player
                self.ended = True
                return True

        # check if draw
        if not np.any(self.board == 0):
            # winner stays None
            self.winner = None
            self.ended = True
            return True

        # game is not over
        self.winner = None
        return False

    def draw_board(self, logger_func=print):
        # Example board
        # -------------
        # | x |   |   |
        # -------------
        # |   |   |   |
        # -------------
        # |   |   | o |
        # -------------

        for i in range(Environment.BOARD_LENGTH):
            logger_func("-------------")

            line = "|".join([self.cell_repr[s] for s in [self.board[i, j] for j in range(Environment.BOARD_LENGTH)]])
            line = '|'+line+'|'

            logger_func(line)
        logger_func("-------------")

    def move(self, sym, i, j):
        # Assert correct input
        assert i in range(Environment.BOARD_LENGTH)
        assert j in range(Environment.BOARD_LENGTH)
        assert sym in (Environment.SYMBOL_X, Environment.SYMBOL_O)

        self.board[i, j] = sym

    def take_action(self, sym, action):
        assert action in self.get_possible_moves(), \
            ValueError("Action '%s' doesn't belong to the possible movements: %s",
                       str(action), str(self.get_possible_moves()))
        i, j = action
        self.move(sym, i, j)
        self.actions_taken.append(action)
        reward = self.reward_function(sym)
        state = self.phi_function()
        is_over = self.game_over()

        return state, reward, is_over

    @staticmethod
    def sample_action():
        return np.random.choice(list(Environment.available_actions))

    def render(self):
        return self.board.__repr__()

    def copy(self, deep=True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def reset(self):
        self.board = np.zeros((Environment.BOARD_LENGTH, Environment.BOARD_LENGTH))
        self.actions_taken = []
        self.ended = False
        self.winner = None

