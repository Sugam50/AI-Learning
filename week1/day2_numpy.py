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


print(np.mean(a)) # 5.5
sum = 0;
for i in a:
    sum += i
mean = sum / len(a);
print(mean); # mean

print(np.var(a)) # 11.916666666666666
sum = 0;
for i in a:
    sum += (i - mean) ** 2
print(sum / len(a)); # variance
variance = sum / len(a);
print(variance)

print(np.std(a)) # 3.452052529534663
standard_deviation = math.sqrt(variance);
