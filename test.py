import matplotlib.pyplot as plt

l = [((1,0),4),((0,1),8), ((2,1),2),((3,1),5),((4,2),7),((3,0),3)] 
l = [ (1.0, 2), (2.0, 3), (1, 3), (3, 1), (4, 2), (1, 2)]

print(l)
fig, ax = plt.subplots()
ax.bar(range(len(l)), [t[1] for t in l]  , align="center")
ax.set_xticks(range(len(l)))
ax.set_xticklabels([t[0] for t in l])

plt.show()