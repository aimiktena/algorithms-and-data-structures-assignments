import math
import argparse
from collections import deque

MAX_FLOAT = float('inf')

def calculateTransitionCost(i, j, gamma, n):
    if j<=i:
        return 0
    else: 
        return gamma * (j-i) * math.log(n)

def calculateMessageCost(diff, lamda):
    expdist_value = exponential_distribution(diff, lamda)
    if expdist_value > 0:
        return -math.log(expdist_value)
    else:
        return MAX_FLOAT

def exponential_distribution (x, lamda): 
    return lamda * math.exp(-lamda * x)

def createGraph(n, timestamps, k, lamdas, gamma):
    states_listed = range(k)
    nodes = [(t, state) for state in states_listed for t in range(len(timestamps))]
    edges = {node: [] for node in nodes}

    for t in range(1, len(timestamps)):
        for i in states_listed: #i: current state
            current_node = (t - 1, i)
            for j in states_listed: #j: next state
                next_node = (t, j)
                interval_period = timestamps[t] - timestamps[t - 1]
                transition_cost = calculateTransitionCost(i, j, gamma, n)
                message_cost = calculateMessageCost(interval_period, lamdas[j])
                total_cost = transition_cost + message_cost
                edges[current_node].append((next_node, total_cost, transition_cost, message_cost))

    #Remove the incorrect edges for the initial state nodes at t0, keeping only the edges regarding node (t0,q0)
    for state in range(1, k):
        edges[(0, state)] = []

    return edges, nodes

def bellmanford(graph, s):
    nodes = graph.keys()
    dist = {node: MAX_FLOAT for node in nodes}
    dist[s] = 0
    paths = {node: [s] for node in nodes} # Instead of just storing the predecessor, we want to store the full path
    relaxations =[]

    q = deque()
    in_queue = {node: False for node in nodes}
    in_queue[s] = True
    q.append(s)

    while len(q) != 0:
        u = q.popleft()
        in_queue[u] = False

        for v, total_weight, transition_cost, message_cost in graph[u]:
            if dist[u] != MAX_FLOAT and dist[v] > dist[u] + total_weight:
                relaxations.append((v, dist[v], dist[u] + total_weight, u, dist[u], transition_cost, message_cost))
                dist[v] = dist[u] + total_weight
                paths[v] = paths[u] + [v]  

                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True

    return dist, paths, relaxations

def burstsViterbi(n, X, k, lamdas, gamma):
    costs = [[0 if i == 0 and j == 0 else MAX_FLOAT for j in range(k)] for i in range(n + 1)]
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
                costs[t][s] = cmin - math.log(expdist_value)  
            else:
                costs[t][s] = cmin - float('-inf')
            paths[s][0:t] = paths[lmin][0:t]
            paths[s][t] = s

    cmin = costs[n][0] 
    smin = 0 
    for s in range(1, k):
        if costs[n][s] < cmin:
            cmin = costs[n][s]
            smin = s

    S = paths[smin]
    return S, costs

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
    state_at_each_timestamp, costs = burstsViterbi(n, interval_periods, k, lamdas_per_state, gamma)
    
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
            print(f"{current_s} [{start_of_next_s } {end_of_this_s})", sep="")
            current_s = state_at_each_timestamp[t]
            start_of_next_s = timestamps[t - 1]

    end_of_this_s = timestamps[-1]
    print(f"{current_s} [{start_of_next_s } {end_of_this_s})", sep="")

elif args.algorithm == 'trellis':
    graph, nodes = createGraph(n, timestamps, k, lamdas_per_state, gamma)
    starting_node = (nodes[0])  #First node refers to (t0,q0)
    distances, paths, relaxations = bellmanford(graph, starting_node)

    #Find the end node with the minimum distance to find the path of nodes for the shortest path
    end_node = None
    min_distance = MAX_FLOAT
    for state in range(k):
        node = (n, state)
        if distances[node] < min_distance:
            min_distance = distances[node]
            end_node = node
    shortest_path = paths[end_node]

    if args.d:  
        for relaxation in relaxations:
            to_node, previous_distance, new_distance, from_node, cost_from_node, transition_cost, message_cost = relaxation
            print(f"{to_node} {previous_distance:.2f} -> {new_distance:.2f} from {from_node} {cost_from_node:.2f} + {transition_cost:.2f} + {message_cost:.2f}")
        print(len(timestamps), [node[1] for node in shortest_path])

    #Again, starting time and state are standard
    current_s = shortest_path[0][1]
    start_of_next_s = timestamps[shortest_path[0][0]]

    for t in range(1, len(shortest_path)):
        current_node = shortest_path[t]
        next_state = current_node[1]

        if next_state != current_s:
            end_of_this_s = timestamps[current_node[0] - 1]
            print(f"{current_s} [{start_of_next_s} {end_of_this_s})", sep="")
            start_of_next_s = end_of_this_s
            current_s = next_state

    end_of_this_s = timestamps[-1]
    print(f"{current_s} [{start_of_next_s} {end_of_this_s})", sep="")