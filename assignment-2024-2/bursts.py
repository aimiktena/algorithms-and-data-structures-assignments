import math

# i: current state, j: next state, gamma: penalty for moving up a state
def calculateTransitionCost(i, j, gamma, n):
    if j<=i:
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

def burstsViterbi(X, k, lamdas, gamma):
    n = len(X)

    costs = [[0 if i == 0 and j == 0 else float('inf') for j in range(k)] for i in range(n + 1)]
    paths = [[0] * (n + 1) for _ in range(k)]

    for t in range(1, n + 1):
        for s in range(k):
            lmin = 0
            cmin = costs[t - 1][0] + calculateTransitionCost(0, s, gamma, n) # cmin is initially set to the cost of transtitioning from state 0 to state s
            for l in range(1, k):
                c = costs[t - 1][l] + calculateTransitionCost(l, s, gamma, n) 
                if c < cmin:
                    cmin = c
                    lmin = l
            expdist_value = exponential_distribution(X[t - 1], lamdas[s])
            if expdist_value > 0:
                second_value = math.log(expdist_value) 
            else:
                second_value =  second_value = float('-inf')
            costs[t][s] = cmin - second_value
            paths[s][0:t] = paths[lmin][0:t]
            paths[s][t] = s

    cmin = costs[n][0] 
    smin = 0 
    for s in range(1, k):
        if costs[n][s] < cmin:
            cmin = costs[n][s]
            smin = s
            
    S = paths[smin]
    return S, paths