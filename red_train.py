# Implementation of the red evaluation script
# This script is used to evaluate the performance of a red agent against a blue agent
# The blue agent is https://github.com/john-cardiff/-cyborg-cage-2.git
# Modified by Prof. H. Sasahara
import inspect
import time

from CybORG import CybORG, CYBORG_VERSION
from CybORG.Agents import B_lineAgent, SleepAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent
from Wrappers.ChallengeWrapper2 import ChallengeWrapper2
from Agents.MainAgent import MainAgent
from Agents.WrappedAgent import WrappedBlueAgent
from Agents.RedAgent import RedPPOAgent
import random, os, torch

MAX_EPS = 100
agent_name = 'Red'
random.seed(153)


# changed to ChallengeWrapper2
def wrap(env):
    return ChallengeWrapper2(env=env, agent_name=agent_name)

if __name__ == "__main__":
    cyborg_version = CYBORG_VERSION
    scenario = 'Scenario2'
    
    # change checkpoint directory
    folder = 'redppo2'
    ckpt = os.path.join(os.getcwd(), "Models", folder)
    if not os.path.exists(ckpt):
        os.makedirs(ckpt)
    
    # Load scenario
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + f'/Shared/Scenarios/{scenario}.yaml'

    # Load blue agent
    blue_agent = WrappedBlueAgent
    # Set up environment with blue agent running in the background and 
    # red agent as the main agent
    cyborg = CybORG(path, 'sim', agents={'Blue': blue_agent})

    env = ChallengeWrapper2(env=cyborg, agent_name="Red")
    # Change restore to False if you want to start training from scratch
    red_agent = RedPPOAgent(env.observation_space.shape[0], ckpt= os.path.join(ckpt, 'modified_invalid_reward.pth'), restore =True)


    print_interval = 50
    save_interval = 200
    max_episodes = 1000000
    max_timesteps = 30
    # 200 episodes for buffer
    update_timestep = 20000
    running_reward, time_step = 0, 0
    set_of_actions = []
    for i_episode in range(1, max_episodes + 1):
        state = env.reset()
        set_of_actions.clear()
        for t in range(max_timesteps):
            time_step += 1
            action = red_agent.get_action(state)
            set_of_actions.append(action)
            
            try:
                state, reward, done, _ = env.step(action)
            except:
                print("Current Time Step: {}\n{}".format(t, set_of_actions))
                raise "Error"
            
            red_agent.store(reward, done)

            if time_step % update_timestep == 0:
                red_agent.train()
                red_agent.clear_memory()
                time_step = 0

            running_reward += reward

        if i_episode % save_interval == 0:
            torch.save(red_agent.policy.state_dict(), os.path.join(ckpt, 'modified_invalid_reward.pth'))
            print('Checkpoint saved')

        if i_episode % print_interval == 0:
            running_reward = float((running_reward / print_interval))
            print('Episode {} \t Avg reward: {}'.format(i_episode, running_reward))
            running_reward = 0
