#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example of solving a magic cube with Actor-Critic model"""

__author__ = 'leferrad'

from tateti.agent.base import play_one
from tateti.agent.dqn import DQNAgent
from tateti.environment.tictactoe import Environment
from tateti.util.fileio import get_logger

import numpy as np
import random

import argparse


logger = get_logger(name="main", level="debug")


# TODO: this should be in a notebook

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to train an agent to solve Tic-Tac-Toe game")
    parser.add_argument('-g', '--gamma', type=float, dest='gamma', default=0.99, help='Discount factor')
    parser.add_argument('-s', '--seed', type=int, dest='seed', default=123, help='Random seed')
    parser.add_argument('-ne', '--n-epis', type=int, dest='N', default=200, help='Number of episodes to run')
    parser.add_argument('-rm', '--rep-mem', dest='replay_mem', type=int, default=1e3,
                        help='Max amount of sequences to store in experience replay memory')
    parser.add_argument('-sr', '--steps-replay', type=int, dest='sr', default=10,
                        help='Number of steps to wait to apply experience replay')
    parser.add_argument('-rf', '--reward-function', dest='reward_function', default="standard",
                        help='Reward function to use')
    parser.add_argument('-pf', '--phi-function', dest='phi_function', default="scaled",
                        help='Phi function to use')
    parser.add_argument('-o', '--out-model', dest='out_model', default='/tmp/tateti_model.pkl',
                        help='Output path to store resulting model')

    args = parser.parse_args()

    print("Using seed=%i" % args.seed)

    random.seed(args.seed)
    seed = random.randint(0, 1000)

    # TODO: not having deterministic results when strategy_function="boltzmann"

    env = Environment(reward_function=args.reward_function, seed=seed)

    path_to_model = args.out_model

    # Create agent
    N = args.N

    agent1 = (DQNAgent(env=env, gamma=args.gamma, phi_function=args.phi_function, strategy_function="egreedy",
                       memory_size=args.replay_mem, batch_size=args.sr)
              #.load(path_to_model)
              )

    agent2 = (DQNAgent(env=env, gamma=args.gamma, phi_function=args.phi_function, strategy_function="egreedy",
                       memory_size=args.replay_mem, batch_size=args.sr)
              #.load(path_to_model)
              )

    max_movements_for_cur_iter, max_movements_for_random = 0, 0
    total_rewards = {Environment.SYMBOL_X: np.empty(N), Environment.SYMBOL_O: np.empty(N)}
    total_iters = np.empty(N)
    total_games = np.empty(N)

    for n in range(N):
        total_reward, iters, is_over = play_one(agent1, agent2, env)

        for sym in total_reward:
            total_rewards[sym][n] = total_reward[sym]

        total_iters[n] = iters
        total_games[n] = int(is_over)

        if n % 10 == 0:
            # logger.info("Episode:%i, total reward: %s, avg reward (last 10): %s, avg games solved (last 10): %s",
            #             n, total_reward, total_rewards[max(0, n-10):(n+1)].mean(),
            #             total_games[max(0, n-10):(n+1)].mean())
            env.draw_board(logger_func=logger.info)
            logger.info("Score board: %s", str(env.score))

        seed = random.randint(0, 1000)

        env.reset()

    # logger.info("avg reward for last 10 episodes: %s", total_rewards[-10:].mean())
    # logger.info("total steps: %s", total_rewards.sum())

    # plot(y=total_rewards, title="Rewards", show=True)

    # plot_moving_avg(total_rewards, title="Total rewards per episode- moving average")
    # plot_moving_avg(total_iters, title="Total iterations per episode - moving average")
    # plot_moving_avg(total_games, title="Total games solved - moving average")

    logger.info("Saving model on %s..." % path_to_model)

    agent = agent1  # TODO: get the best agent from matches won

    agent.save(path_to_model)

    logger.info("Done!")
