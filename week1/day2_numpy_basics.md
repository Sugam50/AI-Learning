axis = dimensions
nparray.ndim --> gives number of dimensions
nparray.shape(m,n) --> gives size of each dimensions therefore length = shape = num of dim
nparray.size --> total number of elements = (m*n)


Q1) Why does variance square differences?
Ans) To make sure the differences does not go in negative

Find the variance of the following dataset {4, 8, 6, 5, 3, 7} with mean = 5.5.

σ2 = (4 - 5.5)2 + (8 - 5.5)2 + (6−5.5)2 + (5−5.5)2 + (3−5.5)2 + (7- 5.5)2 / 6
σ2 = 17.5/6 = 2.92

std deviation = root of σ
mean = avg


Q2) What breaks if you don’t normalize data?
Ans) The mean variance and standard deviation will have error as the data will have negative values causing the issue
