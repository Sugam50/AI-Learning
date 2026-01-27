import numpy as np

a = np.arange(12);
print(a)
b = a.reshape(2,3,2) # 2*3*2 = 12
# [[[ 0  1]
#   [ 2  3]
#   [ 4  5]]

#  [[ 6  7]
#   [ 8  9]
#   [10 11]]]
# print(np.sum(a))
print(np.sum(b, 2))
print(b)
# print(a.shape)
# print(b.shape)

# Broadcasting example 1
a = np.array([[ 0.0,  0.0,  0.0],
              [10.0, 10.0, 10.0],
              [20.0, 20.0, 20.0],
              [30.0, 30.0, 30.0]])
c = np.array([1.0, 2.0, 3.0, 4.0])
b = np.array([[1.0], 
              [2.0], 
              [3.0], 
              [4.0]])

print(a + c)
