import matplotlib.pyplot as plt
from math import log

X = range(50, 700)

Y = []

for x in X:
    if x == 0:
        Y.append(0.0)
    else:
        Y.append(log(x, 8))


plt.figure(figsize=(9,6))

plt.plot(X,Y)
# plt.xticks([])
plt.yticks([])
plt.xlabel('Sample Rate', fontsize=18)
plt.ylabel('Deduplication Ration', fontsize=18)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.savefig("non_optimal.pdf")
plt.show()