import os

def solve():
  file_name = 'vertex/input.txt'

  if not os.path.exists(file_name):
    print(f'файл {file_name} не найден')
    return

  with open(file_name, 'r', encoding='utf-8') as f:
    tokens = f.read().split()

  if not tokens:
    return

  N = int(tokens[0])
  parent = list(range(N + 1))

  def find(i):
    if parent[i] == i:
      return i
    return find(parent[i])

  groups = N
  for k in range(1, len(tokens), 2):
    u = int(tokens[k])
    v = int(tokens[k + 1])

    root_u = find(u)
    root_v = find(v)

    if root_u != root_v:
      parent[root_u] = root_v
      groups -= 1

  print(groups - 1)


if __name__ == '__main__':
  solve()