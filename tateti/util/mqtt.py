#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tateti.util.fileio import get_logger

import paho.mqtt.client as mqtt

import time

logger = get_logger(name=__name__, level='debug')


class MQTTClient(object):
    rc_dict = {
        0: "Connection successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier",
        3: "Connection refused - server unavailable",
        4: "Connection refused - bad username or password",
        5: "Connection refused - not authorized",
        6: "Currently not used",
    }

    def __init__(self, host, port, max_buffer=4):
        self.host = host
        self.port = port

        self.client = mqtt.Client()
        self.connected = True

        self.client.msgs_queue = []
        self.client.max_buffer = max_buffer  # Max amount of messages to persist on

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_publish = on_publish
        self.client.on_message = on_message

    def connect(self):
        try:
            self.client.connect(self.host, int(self.port), 60)
            logger.debug("MQTTclient connected")
            self.client.loop_start()
            self.connected = True
            return self.connected
        except Exception as e:
            logger.debug("Error while connecting to local broker: %s", str(e))
            logger.debug("Retrying connection...")
            time.sleep(.1)
            self.connect()

    def disconnect(self):
        self.client.disconnect()
        self.connected = False

    def publish(self, topic, payload):
        if self.connected:
            result, mid = self.client.publish(topic, payload, 0)
            return result, mid

    def subscribe(self, list_topics=None):
        if list_topics is None:
            list_topics = []
        subs = []
        for topic in list_topics:
            subs.append((str(topic), 1))
        self.client.subscribe(subs)

    def get_message(self):
        if self.client.msgs_queue:
            return self.client.msgs_queue.pop(0)
        return None


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    client.logger.debug("MQTT Connected with result %s" % str(MQTTClient.rc_dict[rc]))
    if rc == 0:
        client.connected = True


def on_disconnect(client, userdata, rc):
    client.logger.debug("MQTT Disconnected with result code: %s  client:%s, userdata: %s" %
                        (rc, str(client), str(userdata)))
    client.connected = False


def on_publish(client, userdata, mid):
    client.logger.debug("MQTT Message %s published.", str(mid))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print("Message received on topic " + msg.topic + " with QoS " + str(msg.qos) + " and payload " + msg.payload)
    client.msgs_queue.append(msg)
    if len(client.msgs_queue) > client.max_buffer:
        # Assert a max of 'client.max_buffer' messages
        # Just a single pop (it shouldn't accumulate more than 1 message with this function)
        client.msgs_queue.pop(0)
