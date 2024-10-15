from collections import deque


def graph(*args):
    seen = set()
    q = deque(args)
    print("digraph {")
    print("rankdir=LR")
    while q:
        node = q.popleft()
        if node in seen:
            continue

        for reader in node.readers:
            print(f"{node.name} -> {reader.name}")
            q.append(reader)
    print("}")



