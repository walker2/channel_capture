import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
from collections import Counter, OrderedDict
from itertools import groupby
import os
import re
import pickle

# Number of requests
#N = 20000
# Number of users
#M = 10
# Time of service
T = 1   # Determined

#PMAX = 0.35
#PMIN = 0.05

# Request structure


class Req:
    def __init__(self, num, time_in):
        self.num = num
        self.time_in = time_in
        self.time_out = 0


class User:
    def __init__(self, num, lamda, N, M, PMAX, PMIN, cheater=False):
        self.num = num
        self.last_window = True
        self.last_prob = 1
        self.queue = deque()
        self.requests = []
        self.req_num = 0
        self.PMAX = PMAX
        self.PMIN = PMIN
        self.cheater = cheater

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
            if self.cheater:
                prob = 1
            else:
                prob = self.PMAX
        else:
            prob = max(self.last_prob / 2, self.PMIN)

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

class Success:
    def __init__(self, user, window, lamda):
        self.user = user
        self.window = window
        self.lamda = lamda


def simulate(N, M, PMAX, PMIN, cheater=False):
    exp_d = []
    output_stream = []
    X = np.arange(0.04, 0.4, 0.04)

    list_of_successes = []
    users_sent = []
    for lamda in X:
        print('lambda:', lamda)
        users = []

        if not cheater:
            for i in range(1, M):
                users.append(User(i, lamda, N, M, PMAX, PMIN))
        else:
            users.append(User(1, lamda, N, M, PMAX, PMIN, cheater=True))
            for i in range(2, M):
                users.append(User(i, lamda, N, M, PMAX, PMIN))

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
                list_of_successes.append(Success(sending[0].num, window, lamda))
                users_sent.append(sending[0].num)
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

    print('Total number of successes', len(list_of_successes))

    print('Number of successes for each user')
    users_sent = np.array(users_sent)
    count = Counter(users_sent)
    oredered_user_sent = dict(OrderedDict(count))
    #print(list(oredered_user_sent))


    #for success in sent_user_num:
    #    print(success.user, success.window, success.lamda)

    print('Longest streaks')

    lst = []
    last_user_num = -1
    last_user = list_of_successes[0]
    streak = 0
    cnt = 0
    for success in list_of_successes:
        if last_user.user == success.user:
            streak += 1
        else:
            num, count, window, lamda = last_user.user, streak, '{}-{}'.format(last_user.window - streak, last_user.window), last_user.lamda
            lst.append((num, count, window, lamda))
            streak = 1

        cnt += 1
        last_user = success

    print('Convolute list length', len(lst))
    streaks = []
    sorted_lst = sorted(lst, key=lambda tup: tup[1], reverse=True)
    counter = 0
    cnt = 0
    for item in sorted_lst:
        count = item[1]
        if cnt < 25:
            streaks.append(item)
            cnt += 1
        counter += count
    #cnt = 0
    #for item in lst:
    #    count = item[1]
    #    if count > 20:
    #        streaks.append(item)
    #    cnt += count

    print('Mean of values', counter / len(lst))

    maxx = max([item[1] for item in lst])
    print('Your longest run was {}'.format(maxx))

    dirname = 'datapr_{0:.2f}'.format(round(PMAX, 2) * 100)
    if cheater: 
        dirname = 'cheater'

    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    pickle.dump(lst, open(dirname + '/conv_list.dump', 'wb'))
    pickle.dump(streaks, open(dirname + '/streaks.dump', 'wb'))
    pickle.dump(output_stream, open(dirname + '/output.dump', 'wb'))
    
    #retrvd = pickle.load(open(dirname + '/conv_list.dump', 'rb'))
    
    #np.savetxt(dirname + '/conv_list', lst)
    #np.savetxt(dirname + '/streaks', streaks)
    #np.savetxt(dirname + '/output', output_stream)

    plt.figure()
    plt.plot(X, output_stream, label='output')
    plt.plot(X, X, label='input')
    plt.xlabel('lambda')
    plt.ylabel('output lambda')
    plt.title('Lambda')
    plt.savefig(dirname + '/outlambda.png')
    plt.close()

    plt.figure()
    plt.plot(X, exp_d, label='experimental')
    plt.xlabel('lambda')
    plt.ylabel('d')
    plt.title("Sync")
    plt.legend()
    plt.savefig(dirname + '/delay.png')
    plt.close()

    pickle.dump(exp_d, open(dirname + '/delay.dump', 'wb'))

    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(range(len(oredered_user_sent)), [v for k,v in oredered_user_sent.items()], width=0.85, align='center', linewidth=0)
    ax.set_xticks(range(len(oredered_user_sent)))
    ax.set_xticklabels([int(k) for k,v in oredered_user_sent.items()])
    plt.ylabel('Successes series')
    plt.xlabel('User number')

    fig = plt.gcf()
    fig.set_size_inches(16, 10)
    fig.savefig(dirname + '/hist.png', dpi=50)
    plt.close()

    return [len(list_of_successes), len(lst)]

def plot_streaks(PMAX, cheater=False):
    dirname = 'datapr_{0:.2f}'.format(round(PMAX, 2) * 100)
    if cheater: 
        dirname = 'cheater'

    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    streaks = pickle.load(open(dirname + '/streaks.dump', 'rb'))

    plt.figure()
    fig, ax = plt.subplots()
    bar1 = ax.bar(range(len(streaks)), [t[1] for t in streaks], width=0.95, align='center', linewidth=0)
    ax.set_xticks(range(len(streaks)))
    ax.set_xticklabels([int(t[0]) for t in streaks])
    plt.ylabel('Successes series')
    plt.xlabel('User number')

    cnt = 0
    last_height = 0

    for rect in bar1:
        height = rect.get_height()
    
        window = re.split('-', streaks[cnt][2])
        plt.text(rect.get_x() + rect.get_width()/2.0, height, window[0] + '\n' + window[1] + '\n' + '{:,.2f}'.format(streaks[cnt][3]), ha='center', va='bottom', fontsize=9)
        
        cnt += 1

    fig = plt.gcf()
    fig.set_size_inches(24,10)
    fig.savefig(dirname + '/highestseries.png', dpi=100)
    plt.close()

    

def plot_first_and_last(PMAX, cheater=False):
    plot_length = 100

    dirname = 'datapr_{0:.2f}'.format(round(PMAX, 2) * 100)
    if cheater: 
        dirname = 'cheater'
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    lst = pickle.load(open(dirname + '/conv_list.dump', 'rb'))

    left_borders = [0, len(lst) - plot_length]

    for border in left_borders:
        slc = lst[border:border + plot_length]

        plt.figure()
        fig, ax = plt.subplots()
        ax.bar(range(len(slc)), [t[1] for t in slc], width=0.85, align='center', linewidth=0)
        ax.set_xticks(range(len(slc)))
        ax.set_xticklabels([int(t[0]) for t in slc])
        plt.ylabel('Successes series')
        plt.xlabel('User number')

        fig = plt.gcf()
        fig.set_size_inches(16, 10)
        fig.savefig(dirname + '/border_{}.png'.format(border), dpi=100)
        plt.close()


