import numpy as np
from collections import deque

# Number of users
M = 20
# Time of service
T = 1   # Determined

lamda = 0.2

PMAX = 0.95
PMIN = 0.05

class User:
    def __init__(self, num):
        self.num = num
        self.last_window = True
        self.last_prob = 1
        self.queue = deque()

    def simulate_window(self):        
        prob = 0
        # Check if last_window was a success
        if self.last_window: 
            prob = PMAX
        else:
            prob = max(self.last_prob / 2, PMIN)
        
        self.last_prob = prob

        rand = np.random.random()

        return rand < prob

    
    def has_message(self):
        # Check if we have new message 
        Y = np.random.exponential(scale=1 / lamda)
        # Add new message to the queue if needed
        
        return self.queue == True
        

users = []
for x in range(0, M):
    users.append(User(x))

users_sending = []
user_succ = False
was_confl = False

for user in users:
    if user.has_message() and user.simulate_window():
        users_sending.append(user)
        
        if user_succ:
            was_confl = True    
        else:
            user.last_window = True
            user_succ = user

if was_confl:
    for user in users_sending:
        user.last_window = False


    