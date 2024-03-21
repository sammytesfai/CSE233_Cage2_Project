from CybORG.Agents import BaseAgent
from CybORG.Shared.Actions import Sleep

# Takes in either Bline or RedMeanderAgent for the agent argument
class LateStartAgent(BaseAgent):
    def __init__(self, agent) -> None:
        super().__init__()
        self.action_count = 0
        # turns out you only need to sleep for 2 turns before acting.
        self.sleep = 2
        self.agent = agent
        self.initial_observation = None

    def get_action(self, observation, action_space):
        """gets an action from the agent that should be performed based on the agent's internal state and provided observation and action space"""
        session = list(action_space['session'].keys())[0]

        if self.action_count == 0:
            self.initial_observation = observation
        elif self.action_count == self.sleep:
            observation = self.initial_observation

        action = Sleep()
        if self.action_count < self.sleep:
            self.action_count += 1
        else:
            # imitate chosen red agent
            action = self.agent.get_action(observation=observation, action_space=action_space)

            self.action_count += 1
        return action

    # Not implemented since this agent does not need a trained model.
    def train(self):
        """allows an agent to learn a policy"""
        raise NotImplementedError

    # Reset the agent for the next epsiode.
    def end_episode(self):
        self.action_count = 0
        self.initial_observation = None
        self.agent.end_episode()