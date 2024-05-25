import math
import argparse

# i: current state, j: next state, gamma: penalty for moving up a state
def calculateTransitionCost(i, j, gamma, n):
    if j<=i:
        return 0
    else: 
        return gamma * (j-i) * math.log(n)

def calculateMessageCost(diff, lamda):
    return -math.log(exponential_distribution(diff, lamda))

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
    return S, paths, costs

parser = argparse.ArgumentParser()
parser.add_argument('algorithm')
parser.add_argument('file', type= str)
parser.add_argument('-s', type= float, default=2)
parser.add_argument('-g', '--gamma', type= float, default=1)
parser.add_argument('-d', action='store_true')

args = parser.parse_args()

with open(args.file, 'r') as file:
    timestamps = [float(timestamp) for timestamp in file.read().split()]

interval_periods = []
for n in range(1, len(timestamps)):
    interval_periods.append(timestamps[n] - timestamps[n-1])

min_interval = min(interval_periods)

n = len(timestamps) - 1
T = timestamps[n] - timestamps[0]

s = args.s
gamma = args.gamma

k = math.ceil(1 + (math.log(T) / math.log(s)) + (math.log(1 / min_interval) / math.log(s))) 
g= T/n

lamdas_per_state = []
for i in range(k):
    lamdas_per_state.append((s ** i) / g)

if args.algorithm == 'viterbi':
    state_at_each_timestamp, paths, costs = burstsViterbi(interval_periods, k, lamdas_per_state, gamma)
elif args.algorithm == 'trellis':
    pass # For now

if args.d:
    for row in costs:
        print([round(cost, 2) for cost in row])
    print(len(timestamps), state_at_each_timestamp)

# Starting time and state are standard
current_s = state_at_each_timestamp[0]
start_of_next_s = timestamps[0]

for t in range(1, n+1):
    if state_at_each_timestamp[t] != current_s:
        end_of_this_s = timestamps[t - 1]
        print(current_s, "[", start_of_next_s, end_of_this_s, ")")
        current_s = state_at_each_timestamp[t]
        start_of_next_s = timestamps[t - 1]

end_of_this_s = timestamps[-1]
print(current_s, "[", start_of_next_s, end_of_this_s, ")")