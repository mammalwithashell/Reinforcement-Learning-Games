from collections import defaultdict
import random

class Agent:
    """ this class is a generic Q-Learning reinforcement learning agent for discrete states and fixed actions
    represented as strings"""
    """def __bool__(self):
        return """
    
    
    def __init__(self, difficulty, environment=None, learning_rate = 0.5, discount_factor = 0.95, epsilon = 0.2):
        self.environment = environment
        tempdict = ''
        with open(difficulty, 'r') as f:
            for i in f.readlines():
                tempdict = i
        tempdict = eval(tempdict)
        self.Q = defaultdict(lambda: 0.0, tempdict)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon # Fraction of time making a random choice for epsilon policy
        self.reset_past()

    def reset_past(self):
        self.past_action = None
        self.past_state = None

    def select_action(self):
        print("selecting action...")
        available_actions = self.environment.available_actions()
        Q_vals = [self.Q[(self.environment.get_state(), x)] for x in available_actions]
        #randomly pick one of the maximum values
        max_val = max(Q_vals) # will often be 0 in the beginning
        max_pos = [i for i, j in enumerate(Q_vals) if j == max_val]
        max_indices = [available_actions[x] for x in max_pos]
        choice = random.choice(max_indices)
        self.past_state = self.environment.get_state()
        self.past_action = choice
        return choice

    def reward(self, reward_value):
        # finding the best expected reward
        available_actions = self.environment.available_actions()
        next_Q_vals = [self.Q[(self.environment.get_state(), x)] for x in available_actions]
        max_next_Q = max(next_Q_vals) if next_Q_vals else 0 # will often be 0 in the beginning
        td_target = reward_value + self.discount_factor * max_next_Q
        reward_pred_error = td_target - self.Q[(self.past_state,self.past_action)]
        if (self.past_state or self.past_action):
            self.Q[(self.past_state,self.past_action)] += self.learning_rate * reward_pred_error