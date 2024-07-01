import argparse

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
        graph[v].append(e)