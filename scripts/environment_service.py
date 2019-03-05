# -*- coding: utf-8 -*-

"""Environment of Tic-Tac-Toe game performing MQTT communication"""

__author__ = 'leferrad'

from tateti.environment.tictactoe import Environment
from tateti.util.fileio import get_logger
from tateti.util.mqtt import MQTTClient

import argparse
import json
import os
import random
import time


logger = get_logger(name="main", level="debug")


def get_first_message():
    return {"state": env.get_state(),
            "reward": 0.0,
            "is_over": False,
            "turn": random.choice([p1_topic, p2_topic]),
            "env_str": env.get_env_string()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Environment of Tic-Tac-Toe game performing MQTT communication")
    parser.add_argument('-mb', '--max-buffer', type=int, dest='mqtt_max_buffer', default=4,
                        help='Max of messages to retain on the MQTT queue')
    parser.add_argument('-s', '--seed', type=int, dest='seed', default=123,
                        help='Seed for random methods on Environment')

    args = parser.parse_args()

    MQTT_HOST_ADDRESS = os.environ["MQTT_HOST_ADDRESS"]
    MQTT_HOST_PORT = int(os.environ["MQTT_HOST_PORT"])

    # --- Start MQTT Client ---
    mqtt = MQTTClient(host=MQTT_HOST_ADDRESS, port=MQTT_HOST_PORT, max_buffer=args.mqtt_max_buffer)
    mqtt.connect()

    # Subscribe
    p1_topic = os.environ['MQTT_P1_TOPIC']
    assert p1_topic is not None
    p2_topic = os.environ['MQTT_P2_TOPIC']
    assert p2_topic is not None

    mqtt.subscribe([p1_topic, p2_topic])

    # Create environment, as well as the players
    env = Environment(seed=args.seed)
    player_1 = Environment.SYMBOL_X
    player_2 = Environment.SYMBOL_O

    out_topic = os.environ['MQTT_ENV_TOPIC']

    # -------------------------

    # Send first message of beginning of game
    env_message = get_first_message()
    mqtt.publish(topic=out_topic, payload=json.dumps(env_message))

    # -------------------------

    logger.info("Start looping...")

    while True:
        current_timestamp = time.time()  # TODO: not used
        msg_in = mqtt.get_message()

        if msg_in is not None:
            # New message to process
            topic = msg_in.topic
            msg_in = json.loads(msg_in.payload.decode())  # Payload is in bytes format, so it must be decoded

            logger.debug("A message has been received! Payload: %s", str(msg_in))

            # Recognize player from topic
            if topic == p1_topic:
                player = player_1
            elif topic == p2_topic:
                player = player_2
            else:
                # Not recognized message should be ignored
                continue

            # Check if the input message belongs to the last output message sent
            assert "env_str" in msg_in
            if msg_in["env_str"] != env.get_env_string():
                # Then it is not synchronized with the current status, so it can be discarded
                continue

            # Get the action to take from message
            assert "action" in msg_in
            action = tuple(msg_in["action"])
            # Perform action and get information about the result
            state, reward, is_over = env.take_action(sym=player, action=action)

            # Indicate who is the next player on the output message
            turn = p2_topic if player == player_1 else p1_topic

            env_str = env.get_env_string()

            # TODO: provide result of action taken by player (to learn?)

            # Report current state of environment on 'out_topic'
            env_message = {"state": state, "reward": reward, "is_over": is_over, "turn": turn, "env_str": env_str}
            mqtt.publish(out_topic, payload=json.dumps(env_message))

        # Draw board through logger
        logger.info("Status of board:")
        env.draw_board(logger_func=logger.info)

        if env.game_over():
            # TODO: count matches won by player to make analytics
            logger.info("GAME OVER! Winner: %s", str(env.winner))
            logger.info("Now restarting game ...")
            env.reset()

            # Get first message of the game
            env_message = get_first_message()

        # Report last state of environment on 'out_topic', as a continuous ping
        mqtt.publish(out_topic, payload=json.dumps(env_message))

        # One second of delay to easily follow the game status
        time.sleep(1)
