# Project 2: Multi-Agent Search
---
Berkeley CS188 Intro to AI in this [link](http://ai.berkeley.edu/search.html)  

In this project, I designed agents for the classic version of Pacman, including ghosts. Along the way, I implemented both minimax and expectimax search.

The code base has not changed much from the previous project, but I started with a fresh installation, rather than intermingling files from project 1.

As in project 1, this project includes an autograder for autograde the answers on your machine. This can be run on all questions with the command:
```
python autograder.py -q q2
```
## Course corpus
- Q1: Reflex Agent
- Q2: Minimax
- Q3: Alpha-Beta Pruning
- Q4: Expectimax
- Q5: Evaluation Function

## Files edited:
```multiAgents.py```	Where all of your multi-agent search agents will reside.

```pacman.py```	The main file that runs Pacman games. This file also describes a Pacman GameState type, which you will use extensively in this project

```game.py```	The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.

```util.py```	Useful data structures for implementing search algorithms.
