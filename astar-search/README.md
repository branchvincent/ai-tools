# A* Search Algorithm

## General Setup
Python 2.7.13 was chosen as the programming language for this assignment. In addition to Python2, the `numpy` package is also required. This can be installed, if not already, via the following command:
```python
pip install -r requirements.txt
```

Note: The `astar.py` file contains the main search algorithm and base classes that the two problem files inherit from.

## Problem 1: [Knights Problem](https://en.wikipedia.org/wiki/Knight%27s_tour)
For the first problem, you need to run `prob1.py`, which has the following usage:
```python
python prob1.py [-h] [-hr HEURISTIC_FILE] [-o OUTPUT_FILE] f
```
These options are described in more detail using the help flag, `-h`. The only required option is `f`, which is the file containing the initial state.

## Problem 2: [Superqueens Problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
For the second problem, you need to run `prob2.py`, which has the following usage:
```python
python prob2.py [-h] [-o OUTPUT_FILE] sz
```
These options are described in more detail using the help flag, `-h`. The only required option is `sz`, which is the size of the chessboard.
