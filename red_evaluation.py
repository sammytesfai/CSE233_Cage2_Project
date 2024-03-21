# Implementation of the red evaluation script
# This script is used to evaluate the performance of a red agent against a blue agent
# The blue agent is https://github.com/john-cardiff/-cyborg-cage-2.git
# Modified by Prof. H. Sasahara
import inspect
import time
from statistics import mean, stdev

from CybORG import CybORG, CYBORG_VERSION
from CybORG.Agents import B_lineAgent, SleepAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent
from Wrappers.ChallengeWrapper2 import ChallengeWrapper2
from Agents.WrappedAgent import WrappedBlueAgent
from Agents.MainAgent import MainAgent
from Agents.RedAgent import RedPPOAgent
import random, os

MAX_EPS = 100
agent_name = 'Red'
random.seed(153)


# changed to ChallengeWrapper2
def wrap(env):
    return ChallengeWrapper2(env=env, agent_name=agent_name)

if __name__ == "__main__":
    cyborg_version = CYBORG_VERSION
    scenario = 'Scenario2'
    # commit_hash = get_git_revision_hash()
    
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
    
    red_agent = RedPPOAgent(env.observation_space.shape[0], ckpt= os.path.join(ckpt, 'modified_invalid_reward2.pth'), restore =True)

    num_steps = 30
    observation = env.reset()

    # action_space = wrapped_cyborg.get_action_space(agent_name)
    action_space = env.get_action_space(agent_name)
    total_reward = []
    actions = []
    action_set = []
    for i in range(MAX_EPS):
        r = []
        a = []
        for j in range(num_steps):
            action = red_agent.get_action(observation)
            action_set.append(action)
            observation, rew, done, info = env.step(action)
            r.append(rew)
            a.append((str(env.get_last_action('Blue')), str(env.get_last_action('Red')), action, rew))
        total_reward.append(sum(r))
        actions.append(a)
        observation = env.reset()

    # for a in actions:
    #     for b in a:
    #         print(b)
    #     print("")

    print("Average Total Rewards: {}".format(sum(total_reward)/len(total_reward)))