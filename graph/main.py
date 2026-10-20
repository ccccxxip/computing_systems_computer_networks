import sys
from collections import defaultdict

def has_4_cycle(adj):
    common_neighbors = defaultdict(int)
    
    for u in adj:
        neighbors = list(adj[u])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                v, w = neighbors[i], neighbors[j]
                
                pair = (min(v, w), max(v, w))
                common_neighbors[pair] += 1
                
                if common_neighbors[pair] >= 2:
                    return True
    return False

def solve(filename):
    with open(filename, 'r') as f:
        lines = f.read().split()
        
    if not lines:
        return

    num_graphs = int(lines[0])
    idx = 1
    
    results = []
    
    for _ in range(num_graphs):
        if idx >= len(lines): break
        
        num_vertices = int(lines[idx])
        num_edges = int(lines[idx+1])
        idx += 2
        
        adj = defaultdict(set)
        
        for _ in range(num_edges):
            u = int(lines[idx])
            v = int(lines[idx+1])
            idx += 2
            
            adj[u].add(v)
            adj[v].add(u)
            
        if has_4_cycle(adj):
            results.append("1")
        else:
            results.append("-1")
            
    print(" ".join(results))

if __name__ == '__main__':
    solve('graph/square_graph_dataset.txt')

# ответ получился такой: -1 -1 -1 1 1 -1 1 1 -1 -1 1 1 1 1 -1 -1 -1