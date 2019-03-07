#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for plotting results"""

__author__ = 'leferrad'

import numpy as np
import matplotlib.pyplot as plt


def plot_moving_avg(total_rewards, title='', show=True):
    # See https://github.com/lazyprogrammer/machine_learning_examples/blob/master/rl2/cartpole/q_learning_bins.py
    N = len(total_rewards)
    moving_avg = np.empty(N)
    for t in range(N):
        moving_avg[t] = total_rewards[max(0, t-100):(t+1)].mean()
    plt.plot(moving_avg)
    plt.title(title)
    if show:
        plt.show()


def plot(y, x=None, title='', show=True):
    if x is None:
        x = range(len(y))

    plt.plot(x, y)
    plt.title(title)

    if show:
        plt.show()
