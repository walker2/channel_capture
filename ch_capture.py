import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
from collections import Counter, OrderedDict
from itertools import groupby

# Number of requests
N = 20000
# Number of users
M = 10
# Time of service
T = 1   # Determined

PMAX = 1
PMIN = 0.05

# Request structure


class Req:
    def __init__(self, num, time_in):
        self.num = num
        self.time_in = time_in
        self.time_out = 0


class User:
    def __init__(self, num, lamda):
        self.num = num
        self.last_window = True
        self.last_prob = 1
        self.queue = deque()
        self.requests = []
        self.req_num = 0

        # Generate poisson values
        Y = np.random.exponential(scale=M / lamda, size=N)
        self.__createRequests__(Y)

    def __createRequests__(self, Y):
        time = 0
        num = 0
        for y in Y:
            num += 1
            time += y
            self.requests.append(Req(num, time))

    def coin_flip(self):
        prob = 0
        # Check if last_window was a success
        if self.last_window:
            prob = PMAX
        else:
            prob = max(self.last_prob / 2, PMIN)

        self.last_prob = prob

        rand = np.random.random()

        return rand < prob

    def update_queue(self, win_num):
        # Check if we have new message
        while self.req_num < len(self.requests) and self.requests[self.req_num].time_in < (win_num * T + 1):
            # The we have new request
            self.queue.appendleft(self.requests[self.req_num])
            self.req_num += 1

    def send_message(self, win_num):
        self.last_window = True
        request = self.queue.pop()
        request.time_out = win_num * T + 1

exp_d = []
output_stream = []
X = np.arange(0.04, 0.6, 0.04)

sent_user_num = []
for lamda in X:
    print('lambda:', lamda)
    users = []

    #start = time.time()
    for i in range(0, M):
        users.append(User(i, lamda))
    #print('User creation', time.time() - start)

    #start = time.time()
    output = 0
    for window in range(0, N):
        # New window
               
        sending = [] # Array of all users that sending in this window
        # Check users for messages
        for user in users:
            if user.queue: # Check if user has a not empty queue
                # Then we have a candidate for this window
                # And we should flip coin for this user
                if user.coin_flip(): 
                    sending.append(user) # Success this user will be sending in current window

        count = len(sending)
        if count == 0: # We have an EMPTY window, do nothing
            pass
        elif count == 1: # Only one user is sending, so we sending message. SUCCESS
            output += 1
            sending[0].send_message(window)
            sent_user_num.append(sending[0].num)
        else: # CONFLICT
            for user in sending:
                user.last_window = False

        # Update our user queues 
        for user in users:
            user.update_queue(window)

    
    #print('All windows', time.time() - start)
    D = 0

    for user in users:
        sent = 0
        for item in user.requests:
            if item.time_out:
                D += item.time_out - item.time_in
                sent += 1
        if sent:
            D /= sent

    print('D is:', D)
    exp_d.append(D)
    output_stream.append(output / N)


sent_user_num = np.array(sent_user_num)
count = Counter(sent_user_num)
print(OrderedDict(count))

print('Longest streaks')
lst = []
for n,c in groupby(sent_user_num):
   num,count = n,sum(1 for i in c)
   lst.append((num,count))

streaks = []
for n,c in lst:
    if c > 20:
        print(n,":",c)
        streaks.append((n,c))


maxx = max([y for x,y in lst])
print('Your longest run was {}'.format(maxx))
np.savetxt('data/sent_user', sent_user_num)
np.savetxt('data/streaks', streaks)
#plt.plot(X, exp_d, label='experimental')
#plt.xlabel('lambda')
#plt.ylabel('d')
#plt.title("Sync")
#plt.legend()
#plt.savefig("M=20_Pr=95_Max04.png")
plt.figure(2)
plt.plot(X, output_stream, label='output')
plt.plot(X, X, label='input')
plt.xlabel('lambda')
plt.ylabel('output lambda')
plt.title('Lambda')
plt.savefig('Outlambda.png')
np.savetxt('data/output', output_stream)
