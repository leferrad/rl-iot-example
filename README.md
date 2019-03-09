rl-iot-example
==============

![Logo](docs/imgs/brain-iot.jpg)


*Reinforcement Learning agent to solve Tic-Tac-Toe game, deployed on an IoT environment*

### Description

In this project the idea is to achieve an end-to-end solution of a reinforcement learning program that can play Tic-Tac-Toe in an environment that is deployed with IoT technologies. In particular, the RL agent is based on a DQN and, once it is ready to be used, it interacts with the environment through MQTT messages.


### Scope 

Since this is just an example to see how a reinforcement learning program can be deployed as an IoT solution, this is the following scope inteded:

- Just for simplicity, Tic-Tac-Toe was chosen due to be an easy game with few states to explore (i.e. allows quick debugging).
- There are many kinds of RL agents to try, but DQN was a safe option due to be very popular and easy to develop.
- There are some assumptions about the learning process that were tested during the development (e.g. reward, strategy, etc).


### Setup

**Docker**

To install Docker, here are some guides for each OS:

- **Linux (debian based):** https://docs.docker.com/install/linux/docker-ee/ubuntu/
- **Windows:** https://docs.docker.com/docker-for-windows/install/
- **MacOS:** https://docs.docker.com/docker-for-mac/install/


To install Docker Compose, here is the official guide for every OS: https://docs.docker.com/compose/install/


The solution is composed by several services, that are configured on `docker-compose.yml`:
- **mosquitto:** Message broker to allow MQTT communication between services.
- **environment:** Service that runs the environment to play Tic-Tac-Toe game via MQTT.
- **trainer:** Jupyter service to train a RL agent through a convenient notebook.
- **agent1:** Service to load a RL agent as Player 1 ready to play the game through MQTT messages.
- **agent2:** Service to load a RL agent as Player 2 ready to play the game through MQTT messages.

To run the whole solution with these services, follow these instructions:

```
# Steps:
# 1) Build containers (just once)
# $ docker-compose build --no-cache
# 2) Run containers (every time needed)
# $ docker-compose up -d
# -> For 'trainer', on browser go to http://localhost:8888 and access with password 'dqntr41n3r'
# 3) Access to bash of some container
# $ docker exec -it trainer bash
# 4) Stop containers
# $ docker-compose stop
```

If you want to try the package locally, as with any Python library run the following snippet to install it:

> NOTE: Using Python3 that is the supported version

```
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

To check that the library was installed, you should be able to run this command in Python without errors:

```python3
import tateti
```


### Reinforcement Learning 

For more details about the solution in terms of Reinforcement Learning, check `docs/rl-agent.md`


### Next steps

- Better documentation (especially docstrings on code)
- More testing about parameters and learning process of agents
- UI rendering through Flask
- Test more RL algorithms (e.g. agents, strategies, etc)
- Service for human players


### Resources

- **Book:** Sutton, R. S., & Barto, A. G. (1998). *Reinforcement learning: An introduction.*
- **Courses:**
  - Udemy: "LazyProgrammer" lectures.  
  - edX: Reinforcement Learning Explained (Microsoft: DAT257x)
- **Libraries and frameworks**
  - OpenAI Baselines: https://github.com/openai/baselines
  - ChainerRL: https://github.com/chainer/chainerrl
  - KerasRL: https://github.com/keras-rl/keras-rl


