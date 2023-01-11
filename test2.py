import random
import os

# counter = 0
# filename = open('file{}.csv','w')
# while os.path.isfile(filename.format(counter)):
#     counter += 1
# filename = filename.format(counter)

# i = 0
# while os.path.exists('output%s.csv' % i):
#     i += 1

# filename = open('output%s.csv' % i,'w')

# l1 = []
# l2 = []

# #create 1000 choices for l1 and l2

# l = "ABCDEFGH"

# for i in range (1000):
#     l1.append(random.choice(l))
#     l2.append(random.choice(l))

# #count the number of times a letter was picked
# L1={}
# L2={}

# for x in l1:
#     if x not in L1:
#         L1[x] = 1
#     else:
#         L1[x] += 1

# for x in l2:
#     if x not in L2:
#         L2[x] = 1
#     else:
#         L2[x] += 1

# #format data for output        
# filename.write((''+','+'l1'+','+'l2'+'\n'))
# for x in list(l):
#     filename.write(x+',')
#     val = str(L1[x])
#     filename.write(val+',')
#     val2 = str(L2[x])
#     filename.write(val2+'\n')

# filename.close()

# import numpy as np

# emp_arr = np.array([1])
# flag = not np.any(emp_arr)
# if flag:
#    print('Your array is empty')
# else:
#    print('Your array is not empty')
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors
from matplotlib import rcParams
from matplotlib.animation import PillowWriter
import time 
from itertools import chain
import random

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

mean = np.mean(data)
plt.plot(data)
plt.plot([0, len(data)], [mean, mean])

plt.show()