import sys

import gym  # the environment enabler
import numpy
import pfrl
import torch

import configuration
import intex_experiments
import utilities
from data.db_interface import DBInterface
from intex_env.envs.intex_env import intex_env  # intext environment
from rl.deep_q import q_function
from utilities import ColorPrint as uc

# set parameters based on input arguments from the command line (if any)
args = [arg[2:] for arg in sys.argv[1:] if arg.startswith("--")]
for arg in args:
    parameter, value = arg.split("=")
    if utilities.parameter_category(parameter) == "learning":
        value_type = type(configuration.learning_configurations[parameter])
        configuration.learning_configurations[parameter] = value_type(value)
    elif utilities.parameter_category(parameter) == "exploration":
        value_type = type(configuration.exploration_configurations[parameter])
        configuration.exploration_configurations[parameter] = value_type(value)
    elif utilities.parameter_category(parameter) == "environment":
        value_type = type(configuration.environment_configurations[parameter])
        configuration.environment_configurations[parameter] = value_type(value)
    else:
        continue

if configuration.learning_configurations["nb_threads"] > 0:
    torch.set_num_threads(configuration.learning_configurations["nb_threads"])

dataset = configuration.learning_configurations["dataset"]
algorithm = configuration.learning_configurations["algorithm"]
target_variant = configuration.learning_configurations["target_variant"]
reward_power = configuration.environment_configurations["reward_power"]
trained_model_name = "dqn-agent"
operator_variant = configuration.exploration_configurations["operator_variant"]
reward_variant = configuration.environment_configurations["reward_variant"]

# Define an instance of the INTEX environment
env: intex_env = gym.make('intex-env-v1')
with DBInterface(dataset) as db_interface:
    target_query = intex_experiments.target_query()
    target_element_ids = db_interface.get_target_ids(target_query)

    # Define the starting point and the target of the environment
    env.initialize(k=configuration.exploration_configurations["k"], target_element_ids=target_element_ids,
                   reward_variant=reward_variant, db_interface=db_interface, input_element_selection_strategy=configuration.learning_configurations[
        "input_element_selection_strategy"], eval_mode=True)

    # Define an instance of the deep Q function
    observation_size = configuration.environment_configurations["nb_state_features"]
    # Set episode parameters
    nb_episodes = configuration.learning_configurations["nb_episodes"]
    episode_length = configuration.learning_configurations["episode_length"]
    show_every = configuration.learning_configurations["show_every"]

    epsilon_strategy = configuration.learning_configurations["epsilon_strategy"]
    if epsilon_strategy == "constant":
        # Set epsilon-greedy as the explorer function
        epsilon = 0
        explorer = pfrl.explorers.ConstantEpsilonGreedy(
            epsilon=epsilon, random_action_func=env.choose_random_action)
    elif epsilon_strategy == "linear decay":
        explorer = pfrl.explorers.LinearDecayEpsilonGreedy(
            configuration.learning_configurations["start_epsilon"],
            configuration.learning_configurations["end_epsilon"],
            nb_episodes * episode_length,
            random_action_func=env.choose_random_action
        )
    else:
        explorer = pfrl.explorers.ExponentialDecayEpsilonGreedy(
            configuration.learning_configurations["start_epsilon"],
            configuration.learning_configurations["end_epsilon"],
            configuration.learning_configurations["epsilon_decay_factor"],
            random_action_func=env.choose_random_action
        )
    # Set the discount factor for future rewards.
    gamma = configuration.learning_configurations["gamma"]

    # Now create an agent that will interact with the environment.
    agent = None
    # As PyTorch only accepts numpy.float32 by default, specify ...
    # a converter as a feature extractor function phi.
    def phi(x): return x.astype(numpy.float32, copy=False)
    if algorithm == "DQN":

        q_function = q_function(observation_size, env.get_action_space_size())
        replay_buffer = pfrl.replay_buffers.ReplayBuffer(capacity=10 ** 5)
        # Use Adam optimizer to optimize the Q function. We set eps=1e-2 for stability.
        optimizer = torch.optim.Adam(q_function.parameters(
        ), lr=configuration.learning_configurations["alpha"], eps=1e-2)
        agent = pfrl.agents.DoubleDQN(q_function, optimizer, replay_buffer, gamma, explorer,
                                      replay_start_size=50, update_interval=1, target_update_interval=100, phi=phi, gpu=-1, recurrent=False)
        network_width = q_function.network_width
    agent.load('model/rural-eon-382/best')
    print(agent)
    with agent.eval_mode():
        for episode in range(1, nb_episodes + 1):
            # Receive the first observation by resetting the environment
            observation = env.reset()

            # return is the sum of all reward
            Return = 0

            # Current time step in the episode
            time_step = 0

            done = reset = False
            # The episode loop
            while not done and not reset:

                # Choose an action based on the initial observation
                action = agent.act(observation)

                # Apply the action and receive the next state (observation) and the reward
                observation, reward, done, _ = env.step(action)
                Return += reward
                time_step += 1

                reset = True if time_step == episode_length else False

                agent.observe(observation, reward, done, reset)

            if episode % show_every == 0:
                targets_found = env.get_found_target_count()
                perc = round(
                    float(targets_found / len(target_element_ids)) * 100, 2)
                uc.print_episode(episode, round(
                    Return, 2), targets_found, perc)

        uc.print_title("run finished.")
