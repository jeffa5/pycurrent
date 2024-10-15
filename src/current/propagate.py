from collections import defaultdict, deque


def propagate(*args):
    g = set()
    deps = defaultdict(set)
    q = deque(args)
    while q:
        node = q.popleft()
        if node in g:
            continue

        g.add(node)

        for reader in node.readers:
            deps[reader].add(node)
            q.append(reader)

    q = deque(args)
    while q:
        node = q.popleft()
        if node not in g:
            # already processed
            continue
        if deps[node]:
            # not ready yet
            q.append(node)
            continue
        g.remove(node)

        node.refresh()
        for reader in node.readers:
            if reader in deps:
                deps[reader].remove(node)
            q.append(reader)

