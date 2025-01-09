'''

https://www.codingame.com/training/easy/plague-jr

'''

import math


def add_to_dic(d, k, v):
    if k not in d:
        edges[k] = [v]
    else:
        edges[k].append(v)
        
    if v not in d:
        edges[v] = [k]
    else:
        edges[v].append(k)
        

def calc(node, edges):
    loops = -1
    neighbors = [node]
    seen = []

    while len(neighbors) > 0:
        news = []
        for ne in neighbors:
            if ne not in seen:
                for x in edges[ne]:
                    if x not in seen:
                        news.append(x)
            seen.append(ne)
        neighbors = list(set(news))
        loops += 1
    return loops
        

n = int(input())
edges = {}
nodes = []
for i in range(n):
    a, b = [int(j) for j in input().split()]
    
    nodes.extend([a, b])
    add_to_dic(edges, a, b)

nodes = set(nodes)
min_loops = math.inf

len_edges = {key: len(value) for key, value in edges.items()}
nodes = [max(len_edges, key=len_edges.get)]
seen = nodes

while True:
    news = []
    if nodes:
        for node in nodes:
            loops = calc(node, edges)
            if loops < min_loops:
                min_loops = loops
                for nod in edges[node]:
                    if nod not in seen:
                        news.append(nod)
        nodes = news
        for new in news:
            seen.append(new)
    else:
        break    
    
print(min_loops)
