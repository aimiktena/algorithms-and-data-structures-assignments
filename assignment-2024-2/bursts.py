import math

# i: current state, j: next state, gamma: penalty for moving up a state
def calculateTransitionCost(i, j, gamma, n):
    if j<=1:
        return 0
    else: 
        return gamma * (j-i) * math.log(n)