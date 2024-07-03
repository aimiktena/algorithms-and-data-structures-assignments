import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('k', type=int)
parser.add_argument('algorithm')
parser.add_argument('probability', type=float)
parser.add_argument('mc', type=int)
parser.add_argument('-r', type=int, default=42) #ALTHOUGH ASSIGNMENT DOESN'T SPECIFY THE DEFAULT VALUE, I ADDED ONE BECAUSE FROM MY UNDERSTANDING THE USER COULD NOT GIVE A RANDOM SEED
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

def greedy_algorithm(graph, seeds, p, mc):
    selected = None
    max_influence = -1
    currentset_influence = monte_carlo(graph, seeds, p, mc) #INFLUENCE FOR CURRENT SEEDS- NODES

    for node in graph:
        if node not in seeds: # EXAMIN EACH NODE BELONGING TO V - SEEDS
            new_seeds = seeds + [node]
            newset_influence = monte_carlo(graph, new_seeds, p, mc) #INFLUENCE FOR EXISTING SEEDS- NODES + POTENTIAL SEED- NODE
            influence_increase = newset_influence - currentset_influence
            if influence_increase > max_influence:
                max_influence = influence_increase
                selected = node
            elif influence_increase == max_influence and node < selected:
                selected = node
    return selected

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