import networkx as nx

file_name = 'weak_pairs/as20000102.txt'

G = nx.read_edgelist(file_name, comments='#', nodetype=int)
G.remove_edges_from(list(nx.selfloop_edges(G)))

for u, v in G.edges():
    if G.degree(u) < 10 or G.degree(v) < 10:
        continue
    
    common_neighbors = set(G[u]) & set(G[v])
    
    if len(common_neighbors) == 0:
        
        G.remove_edge(u, v)

        if nx.has_path(G, u, v):
            path = nx.shortest_path(G, u, v)
            
            print(f"Найдены слабо связанные вершины: {u} и {v}")
            print(f"Степень вершины {u}: {G.degree(u)}")
            print(f"Степень вершины {v}: {G.degree(v)}")
            print(f"Длина обходного пути: {len(path) - 1} ребер")
            print(f"Сам путь: {path}")
            
            break
            
        G.add_edge(u, v)