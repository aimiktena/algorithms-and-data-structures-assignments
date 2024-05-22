import math

# i: current state, j: next state, gamma: penalty for moving up a state
def calculateTransitionCost(i, j, gamma, n):
    if j<=1:
        return 0
    else: 
        return gamma * (j-i) * math.log(n)

def exponential_distribution (x, lamda): 
    if x>=0:
        return lamda * math.exp(-lamda * x)
    else:
        return 0

def calculateExpectedValue(lamda):
    return 1/lamda