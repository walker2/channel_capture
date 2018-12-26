import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
from collections import Counter, OrderedDict
from itertools import groupby

sent_user_num = np.loadtxt('datapr0_35/sent_user', dtype=float)

print('Number of of points', len(sent_user_num))

print('Convert to streaks')
lst = []
for n,c in groupby(sent_user_num):
   num,count = n, float(sum(1 for i in c))
   lst.append((num,count))

print('List length', len(lst))
for i in range(40000, 42000, 100):
    slc = lst[i:i + 100]
    print(slc)

    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(range(len(slc)), [t[1] for t in slc])
    ax.set_xticks(range(len(slc)))
    ax.set_xticklabels([int(t[0]) for t in slc])

#   plt.show()
    fig = plt.gcf()
    fig.set_size_inches(30,10)
    fig.savefig('fig' + str(i / 100) + '.png', dpi=100)
    break