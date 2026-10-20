import sys

matrix = [
    #  A  B  C  D  E  F
    [0, 1, 1, 0, 0, 0],  # A
    [1, 0, 0, 1, 0, 0],  # B
    [1, 0, 0, 0, 1, 0],  # C
    [0, 1, 0, 0, 1, 1],  # D
    [0, 0, 1, 1, 0, 0],  # E
    [0, 0, 0, 1, 0, 0],  # F
]
N = len(matrix)
names = [chr(ord('A') + i) for i in range(N)]

INF = -1 
dist = [INF] * N 


def visit(v, d):
    if dist[v] != INF and dist[v] <= d:
        return 
    dist[v] = d 
    for u in range(N):
        if matrix[v][u] == 1:
            visit(u, d + 1) 


def parse_vertex(text):
    text = text.strip()
    if text.upper() in names:
        return names.index(text.upper())
    if text.isdigit() and int(text) < N:
        return int(text)
    raise ValueError


text = sys.argv[1] if len(sys.argv) > 1 else input('Стартовая вершина K (A-%s или номер 0-%d): ' % (names[-1], N - 1))
try:
    K = parse_vertex(text)
except ValueError:
    sys.exit('Нет такой вершины: ' + text)

sys.setrecursionlimit(N + 100) 
visit(K, 0)

for v in range(N):
    print(names[v], dist[v] if dist[v] != INF else 'нет пути')