1) Why was NumPy faster?
Ans) Due to:
- Contiguos Memory allocation
- Vectorization( Optimised C )
- single data Type

2) Where is the loop actually running?
Ans) Loop is running in both cases but in list the loop is running at python interpreter but in numpy it is running inside builtin C level highly optimised library making it much faster
