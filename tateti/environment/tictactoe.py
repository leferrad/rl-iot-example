# -*- coding: utf-8 -*-

"""Model of the environment that will be used for every agent"""

# NOTE: highly based on https://github.com/lazyprogrammer/machine_learning_examples/blob/master/rl/tic_tac_toe.py

__author__ = 'leferrad'

import numpy as np

import copy
import itertools


def standard_reward(env, sym, reward_positive=1, reward_negative=0):
    reward = reward_negative
    if env.game_over():
        reward = reward_positive if env.winner == sym else reward_negative
    return reward


# TODO: try other reward functions and check what happens!

available_rewards = {'standard': standard_reward}


class Environment(object):
    BOARD_LENGTH = 3  # TODO: parameter of Environment
    SYMBOL_X = -1
    SYMBOL_O = 1
    SYMBOL_EMPTY = 0
    NEGATIVE_REWARD_ILLEGAL_MOVE = -1.0

    available_actions = list(itertools.product(range(BOARD_LENGTH), range(BOARD_LENGTH)))
    n_actions = len(available_actions)
    n_dimensions = BOARD_LENGTH ** 2

    sym_repr = {SYMBOL_X: "x", SYMBOL_O: "o", SYMBOL_EMPTY: " "}

    def __init__(self, reward_function='standard', seed=123):
        self.board = np.zeros((Environment.BOARD_LENGTH, Environment.BOARD_LENGTH))

        self.winner = None
        self.ended = False
        self.num_states = 3 ** (Environment.BOARD_LENGTH * Environment.BOARD_LENGTH)
        
        self.actions_taken = []
        self.score = {k: 0 for k in self.sym_repr.values()}

        assert reward_function in available_rewards
        self.reward_function = lambda sym: available_rewards[reward_function](self, sym)

        # Set seed on random module
        self.seed = seed
        np.random.seed(seed)

        # First player is randomly chosen
        self.turn = np.random.choice([self.SYMBOL_X, self.SYMBOL_O])

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def is_draw(self):
        return self.ended and self.winner is None

    def get_state(self):
        return [int(x) for x in np.nditer(self.board)]

    def get_env_string(self):
        return "".join([self.sym_repr[x] for x in self.get_state()])

    def get_possible_moves(self):
        return [(i, j) for (i, j) in self.available_actions if self.is_empty(i, j)]

    @staticmethod
    def get_possible_moves_from_str(env_str):
        return list(map(lambda x_a: x_a[1],  # Get corresponding action
                        filter(lambda x_a: x_a[0] == " ",  # Get only empty cells
                               # x_a: tuple of (element of cell, action)
                               zip(env_str, Environment.available_actions))))

    def game_over(self):
        # returns true if game over (a player has won or it's a draw)
        # otherwise returns false
        # also sets 'winner' instance variable and 'ended' instance variable

        # check rows
        for i in range(Environment.BOARD_LENGTH):
            for player in (self.SYMBOL_X, self.SYMBOL_O):
                if self.board[i].sum() == player * Environment.BOARD_LENGTH:
                    self.winner = self.sym_repr[player]
                    self.ended = True
                    return True

        # check columns
        for j in range(Environment.BOARD_LENGTH):
            for player in (self.SYMBOL_X, self.SYMBOL_O):
                if self.board[:, j].sum() == player * Environment.BOARD_LENGTH:
                    self.winner = self.sym_repr[player]
                    self.ended = True
                    return True

        # check diagonals
        for player in (self.SYMBOL_X, self.SYMBOL_O):
            # top-left -> bottom-right diagonal
            if self.board.trace() == player * Environment.BOARD_LENGTH:
                self.winner = self.sym_repr[player]
                self.ended = True
                return True
            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player * Environment.BOARD_LENGTH:
                self.winner = self.sym_repr[player]
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
            line = "|".join([" " + self.sym_repr[s] + " " for s in [self.board[i, j]
                                                                    for j in range(Environment.BOARD_LENGTH)]])
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
        assert sym == self.turn

        if action in self.get_possible_moves():
            # Then this is a legal action that will be taken on the env
            i, j = action
            self.move(sym, i, j)
            self.actions_taken.append(action)
            reward = self.reward_function(sym)
            self.turn = self.SYMBOL_X if sym == self.SYMBOL_O else self.SYMBOL_O
        else:
            # Otherwise, 'action' is an illegal move that must be show to the agent with a negative reward
            reward = self.NEGATIVE_REWARD_ILLEGAL_MOVE
            # The turn doesn't change, and no movement is applied to the env

        state = self.get_state()
        is_over = self.game_over()

        if is_over:
            self._update_score()

        return state, reward, is_over, self.turn

    def _update_score(self):
        winner = self.winner if self.winner is not None else self.sym_repr[self.SYMBOL_EMPTY]
        self.score[winner] += 1

    @staticmethod
    def sample_action():
        return np.random.choice(list(Environment.available_actions))

    def render(self):
        return self.draw_board(print)

    def copy(self, deep=True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def reset(self):
        self.board = np.zeros((Environment.BOARD_LENGTH, Environment.BOARD_LENGTH))
        self.actions_taken = []
        self.ended = False
        self.winner = None

        # First player is randomly chosen
        self.turn = np.random.choice([self.SYMBOL_X, self.SYMBOL_O])

