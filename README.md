# Four Russians Implementation

I came across the Four Russians algorithm in [Real World Algorithms](https://louridas.github.io/rwa/assignments/four-russians/), a method for speeding up algorithms involving Boolean matrices. This repository contains a Python implementation of the algorithm in $O(n^2 / lg (n))$ with bitwise operations based on the Exercise [here](https://louridas.github.io/rwa/assignments/four-russians/). 

## Installation

1. Install Python 3.
2. Run `python3 main.py tests/graph_1.txt tests/graph_expected.txt` to test generating the transitive closure of graph 
3. Run `python3 main.py tests/array_1.txt tests/array_2.txt tests/array_expected.txt` to test a simple boolean matrix multiplication.
4. Run `python3 test.py` to run the two test cases above
