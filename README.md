# Algorithms and Data Structures Assignments

This repository contains solutions to the assignments from the **Algorithms and Data Structures** course. The assignments cover a variety of algorithmic problems, with an emphasis on graph theory, optimization, and dynamic modeling. Each assignment demonstrates a practical application of algorithms and their implementation.

## Assignment 1: Tromino Tiling
- **Problem**: Solve the **Tromino Tiling Problem** using recursive division of a square grid to tile it with L-shaped pieces (trominoes), while handling a single missing square.
- **Solution**: The grid is recursively divided into smaller grids, and each grid is tiled with trominoes. The problem is mapped to a **graph coloring problem** to ensure that no two adjacent trominoes share the same color.
- **Technologies**: Python, recursion, grid manipulation, graph coloring

## Assignment 2: Burst Detection
- **Problem**: Given a stream of timestamps, detect periods of **activity bursts** using an **Exponential Distribution** model, and find the minimum-cost paths of state transitions with respect to both transition costs and message costs.
- **Solution**: Implemented a **Viterbi algorithm** and **Bellman-Ford algorithm** to detect bursts and minimize the cost of state transitions. The model calculates transition and message costs based on the input timestamps.
- **Technologies**: Python, dynamic programming (Viterbi, Bellman-Ford), exponential distribution, cost optimization

## Assignment 3: Influence Maximization
- **Problem**: Maximize the spread of influence in a social network using an **Independent Cascade Model**. The task is to identify optimal seed nodes that will maximize the influence spread across the network using a **Monte Carlo simulation**.
- **Solution**: Implemented **greedy** and **max degree** algorithms to select seed nodes for influence maximization. The simulation is run multiple times to estimate the effectiveness of different seed sets.
- **Technologies**: Python, Monte Carlo simulation, greedy algorithm, graph theory

## Technologies Used:
- Python 3.x
- Dynamic programming algorithms (Viterbi, Bellman-Ford)
- Graph theory algorithms (Greedy, Monte Carlo simulations)
- Recursion, cost optimization, exponential distribution
