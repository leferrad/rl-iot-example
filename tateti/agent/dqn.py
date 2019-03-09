# -*- coding: utf-8 -*-

"""DQN Reinforcement Learning Agent"""

__author__ = 'leferrad'

# NOTE: pretty based on https://github.com/gsurma/cartpole/blob/master/cartpole.py

from tateti.agent.base import BaseAgent
from tateti.environment.tictactoe import Environment

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np

from collections import deque
import random


class DQNAgent(BaseAgent):

    def __init__(self, env, model=None, gamma=0.95, phi_function="integer", strategy_function='egreedy',
                 memory_size=400, batch_size=10):
        BaseAgent.__init__(self, env=env, gamma=gamma, phi_function=phi_function, strategy_function=strategy_function)

        self.memory = deque(maxlen=int(memory_size))
        self.batch_size = batch_size

        if model is None:
            model = self._build_default_model(observation_space=self.n_dims, action_space=self.n_actions)

        self.model = model

    @staticmethod
    def _build_default_model(observation_space, action_space, n_hidden=24, activation="relu", lr=1e-3):
        model = Sequential()
        model.add(Dense(n_hidden, input_shape=(observation_space,), activation=activation))
        model.add(Dense(n_hidden, activation=activation))
        model.add(Dense(n_hidden, activation=activation))
        model.add(Dense(action_space, activation="linear"))
        model.compile(loss="mae", optimizer=Adam(lr=lr))

        return model

    def remember(self, state, action, reward, next_state, terminal):
        self.memory.append((state, action, reward, next_state, terminal))

    def act(self, state, env_string, explore=True):
        # Filter available actions to take
        sym_empty = Environment.sym_repr[Environment.SYMBOL_EMPTY]
        available_actions = [i for (i, s) in enumerate(env_string) if s == sym_empty]

        # Get Q-values for available actions
        state_x = self.phi(state)
        q_values = self.predict(state_x)
        q_values = [q_values[i] for i in available_actions]

        # Get index of sampled available action from strategy used
        action_int = self.strategy.sample_action(v=q_values, explore=explore)
        action_int = available_actions[action_int]  # Index of available to index of all actions
        action = Environment.available_actions[action_int]  # Get action to take

        return action

    def predict(self, x):
        if not isinstance(x, np.ndarray):
            x = np.asarray(x)

        if len(x.shape) == 1:
            return self.model.predict(np.expand_dims(x, axis=0))[0]
        else:
            return self.model.predict(x)

    def fit(self, x, q):
        if not isinstance(x, np.ndarray):
            x = np.asarray(x)

        if len(x.shape) == 1:
            x = np.expand_dims(x, axis=0)

        if not isinstance(q, np.ndarray):
            q = np.asarray(q)

        if len(q.shape) == 1:
            q = np.expand_dims(q, axis=0)

        self.model.fit(x, q, verbose=0)

    def experience_replay(self):
        batch = random.sample(self.memory, self.batch_size)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + self.gamma * np.amax(self.predict(state_next)))
            q_values = self.predict(state)

            a = self.actions[action]
            q_values[a] = q_update

            self.fit(state, q_values)

    def update(self, state, action, reward, next_state, terminal):

        self.remember(state, action, reward, next_state, terminal)

        self.strategy.update()

        if len(self.memory) < self.batch_size:
            # Not enough memory to apply experience replay
            return

        self.experience_replay()

