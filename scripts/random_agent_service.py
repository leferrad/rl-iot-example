# -*- coding: utf-8 -*-

"""Agent service to play Tic-Tac-Toe game performing MQTT communication"""

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Agent service to play Tic-Tac-Toe game performing MQTT communication")
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
    env_topic = os.environ['MQTT_ENV_TOPIC']
    assert env_topic is not None

    mqtt.subscribe([env_topic])

    # Create agent
    p = os.environ.get("PLAYER", '1')
    player = Environment.SYMBOL_X if int(p) == 1 else Environment.SYMBOL_O

    out_topic = os.environ['MQTT_P1_TOPIC'] if player == Environment.SYMBOL_X else os.environ["MQTT_P2_TOPIC"]

    # -------------------------

    logger.info("Start looping...")

    while True:
        current_timestamp = time.time()
        msg_in = mqtt.get_message()

        if msg_in is not None:
            # New message to process
            msg_in = json.loads(msg_in.payload.decode())  # Payload is in bytes format, so it must be decoded

            logger.debug("A message has been received! Payload: %s", str(msg_in))

            turn = msg_in["turn"]

            if turn != out_topic:
                continue

            env_str = msg_in["env_str"]

            actions = Environment.get_possible_moves_from_str(env_str)

            # TEST: A random action
            action = random.choice(actions)

            # Include 'env_str' as a way to synchronize this message with the last one sent by the environment
            player_message = {"action": action, "env_str": env_str}
            mqtt.publish(out_topic, payload=json.dumps(player_message))

        # Draw board through logger
        #logger.info("Status of board:")
        #env.draw_board(logger_func=logger.info)

        time.sleep(0.5)
