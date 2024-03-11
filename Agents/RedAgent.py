from CybORG.Agents import BaseAgent
from Agents.RedPPO import RedPPOAgent
import random

class RedAgent(BaseAgent):
    def __init__(self, input_dims, action_space, ckpt) -> None:
        super().__init__()
        self.agent = RedPPOAgent(input_dims, action_space, ckpt=ckpt)

    def get_action(self, observation, action_space):
        return self.agent.get_action(observation)

    def train(self):
        self.agent.train()