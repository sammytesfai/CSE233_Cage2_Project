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
from Agents.RedAgent import RedAgent
from Agents.LateStartAgent import LateStartAgent
import random

MAX_EPS = 500
agent_name = 'Red'
random.seed(153)

# Set this to either RedMeanderAgent() or B_lineAgent()
#chosen_agent = RedMeanderAgent()
chosen_agent = B_lineAgent()

# changed to ChallengeWrapper2
def wrap(env):
    return ChallengeWrapper2(env=env, agent_name=agent_name)

if __name__ == "__main__":
    cyborg_version = CYBORG_VERSION
    scenario = 'Scenario2'
    # commit_hash = get_git_revision_hash()
    

    
    # Load scenario
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + f'/Shared/Scenarios/{scenario}.yaml'
    

    # Load blue agent
    blue_agent = WrappedBlueAgent
    # Load hard coded red agent
    red_agent = LateStartAgent(chosen_agent)

    # Set up environment with blue agent running in the background and 
    # red agent as the main agent
    cyborg = CybORG(path, 'sim', agents={'Blue': blue_agent})
    
    num_steps = 30
    total_reward = []
    for i in range(MAX_EPS):
        observation = cyborg.reset().observation
        action_space = cyborg.get_action_space(agent_name)
        actions = []
        r = []
        a = []
        for j in range(num_steps):
            action = red_agent.get_action(observation=observation, action_space=action_space)
            result = cyborg.step(agent_name, action)
            observation = result.observation
            rew = result.reward
            done = result.done  
            r.append(rew)
            a.append((str(cyborg.get_last_action('Blue')), str(cyborg.get_last_action('Red'))))
        
        total_reward.append(sum(r))
        actions.append(a)

        # Need to do this to reset the Red Agent for the next episode.
        # Not sure if Blue Agent gets reset because the reward for my RedAgent() skyrockets after the first test.
        red_agent.end_episode()
    
    # Print average reward
    print(sum(total_reward) / len(total_reward))