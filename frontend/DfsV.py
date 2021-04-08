from collections import deque

def dfsV(root, f):
    visited = set()
    q = deque()
    q.append(root)
    while q:
        node = q.pop()
        # hash id(node) instead of node ...
        # otherwise may involve deep recursion ...
        # due to __hash__ definition of VAST nodes ...
        # which is a recursive DFS
        if (id(node) not in visited):
            visited.add(id(node))
        else:
            continue
        f(node)
        q.extend(reversed(node.children()))
