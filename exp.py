import numpy as np
import matplotlib.pyplot as plt
from collections import deque

from itertools import groupby

a = [7,7,7,7,8,8,8,7,7,2,2,2,2,1,1,7,7,7,7,7,7]
lst = []
for n,c in groupby(a):
   num,count = n,sum(1 for i in c)
   lst.append((num,count))

for item in lst:
    print(item)


maxx = max([y for x,y in lst])
print('Your longest run was {}'.format(maxx))
