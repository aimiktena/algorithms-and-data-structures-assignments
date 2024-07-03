import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('k', type=int)
parser.add_argument('algorithm')
parser.add_argument('probability', type=float)
parser.add_argument('mc', type=int)
parser.add_argument('-r', type=int)
args = parser.parse_args()

graph = {}
with open(args.file, 'r') as file:
    for line in file:
        v, e = line.strip().split()   
        v, e = int(v), int(e)
        if v not in graph:
            graph[v] = []
        if e not in graph:
            graph[e] = []
        graph[v].append(e)

def max_degree_algorithm(graph, seeds):
    selected = None
    max_degree = -1
    for node in graph:
        if node not in seeds:
            out_degree = len(graph[node])
            if out_degree > max_degree:
                selected = node
                max_degree = out_degree
            elif out_degree == max_degree and node < selected:
                selected = node
    return selected

def maximize_influence(graph, algorithm, p, k, mc):
    seeds = []
    influences = []
    for _ in range(k):
        if algorithm == "max_degree":
            seed = max_degree_algorithm(graph, seeds)
        elif algorithm == "greedy":
            seed = greedy_algorithm(graph, seeds, p, mc)
           
        seeds.append(seed)
        influence = monte_carlo(graph, seeds, p, mc)
        influences.append(influence)
    return seeds, influences

random.seed(args.r)