import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
from collections import Counter, OrderedDict
from itertools import groupby

# Plot all timeline in pieces, like 500-1000 or something. It will be 10 pictures for full dataset 

sent_user_num = np.loadtxt('data/sent_user', dtype=float)

print('Number of of points', len(sent_user_num))
 
print('Convert to streaks')
lst = []
for n,c in groupby(sent_user_num):
   num,count = n, float(sum(1 for i in c))
   lst.append((num,count))

cnt = 0
#print(lst.keys()[lst.values().index(np.median(lst.values()))])
value_mean = np.median(list(dict(lst).values())) 

print('Mean of values', value_mean)

streaks = []
for n,c in lst:    
    if c > value_mean * 2:
        streaks.append((n,c))


print('Number of streaks', len(streaks))
maxx = max([y for x,y in lst])
print('Your longest streak was {}'.format(maxx))
print(streaks)

fig, ax = plt.subplots()
ax.bar(range(len(streaks)), [t[1] for t in streaks]  , align="center")
ax.set_xticks(range(len(streaks)))
ax.set_xticklabels([t[0] for t in streaks])

#plt.show()
plt.savefig('fig.png')
#markerline, stemlines, baseline = plt.stem(x, np.cos(x), '-.')