import numpy as np
import time as time

list = range(1000000);
current_time = time.time();
list2 = [x+1 for x in list];
print(time.time() - current_time); # 0.05411386489868164

current_time = time.time();
l2 = np.arange(1000000);
print(time.time() - current_time); # 0.001132965087890625
