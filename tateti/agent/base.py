# -*- coding: utf-8 -*-

"""Base implementation for Agents that will play Tic-Tac-Toe"""

from tateti.agent import phi
from tateti.agent import strategy
from tateti.environment.tictactoe import Environment
from tateti.util.fileio import get_logger

import numpy as np


logger = get_logger(__name__, level="debug")


available_phis = {"identity": phi.IdentityPhi(n_dims=Environment.n_dimensions),
                  "scaled": phi.ScaledPhi(n_dims=Environment.n_dimensions,
                                          min_value=min(Environment.SYMBOL_X, Environment.SYMBOL_O),
                                          max_value=max(Environment.SYMBOL_X, Environment.SYMBOL_O))}


available_strategies = {"egreedy": strategy.EpsilonGreedy(available_actions=Environment.available_actions,
                                                          exploit_func=lambda v: np.argmax(v[0]),
                                                          epsilon=0.9, decay=0.95),
                        "boltzmann": strategy.Boltzmann(available_actions=Environment.available_actions,
                                                        exploit_func=lambda v: np.argmax(v[0]),
                                                        epsilon=0.9, decay=0.95)}


class BaseAgent(object):
    def __init__(self, env, gamma=0.99, phi_function="scaled", strategy_function='egreedy'):
        self.phi = available_phis[phi_function]
        self.strategy = available_strategies[strategy_function]

        self.actions = dict([(a, i) for (i, a) in enumerate(env.available_actions)])
        self.n_actions = env.n_actions
        self.n_dims = self.phi.n_dimensions
        self.gamma = gamma
        self.model = None

    def act(self, state):
        pass

    def update(self, state, action, reward, next_state, terminal):
        pass

    def save(self, dirname):
        # TODO: pickle whole object
        self.model.save(dirname)

    def load(self, dirname):
        # TODO: unpickle whole object
        self.model.load(dirname)


def play_one(agent_x, agent_o, env):
    observation = env.get_state()

    total_reward = {Environment.SYMBOL_X: 0, Environment.SYMBOL_O: 0}
    steps = 0

    while not env.game_over():

        sym = env.turn
        agent = agent_x if sym == Environment.SYMBOL_X else agent_o

        action = agent.act(observation)

        next_observation, reward, done, turn = env.take_action(sym, action)
        
        total_reward[sym] += reward

        agent.update(state=observation, action=action, reward=reward, next_state=next_observation, terminal=done)

        # env.draw_board(logger_func=logger.info)

        if done:
            logger.info("GAME OVER! Winner: %s" % str(env.winner))

        observation = next_observation
        steps += 1

    return total_reward, steps, env.game_over()
