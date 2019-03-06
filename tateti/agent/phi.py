# -*- coding: utf-8 -*-

"""Module to handle phi functions to transform states of environment that agents process"""

import numpy as np


class IdentityPhi(object):
    def __init__(self, n_dims):
        self.n_dimensions = n_dims

    def __call__(self, obs):
        return np.asarray(obs)


class ScaledPhi(object):
    def __init__(self, n_dims, min_value=-1.0, max_value=1.0):
        # Scale input to range [0, 1]
        self.n_dimensions = n_dims

        assert min_value != max_value
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, obs):
        obs = np.asarray(obs)
        return (obs - self.min_value) / (self.max_value - self.min_value)
