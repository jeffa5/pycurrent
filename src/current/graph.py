from collections import deque


def graph(*args, debug=False):
    q = deque(args)
    lines = []
    lines.append("digraph {")
    lines.append("  rankdir=LR")
    nodes = set()
    edges = set()
    ids = {}
    maxid = 0
    while q:
        node = q.popleft()
        if node in nodes:
            continue
        nodes.add(node)
        ids[node] = maxid
        maxid += 1

        for reader in node.readers:
            edges.add((node, reader))
            q.append(reader)

    for node in nodes:
        if debug:
            lines.append(f"  {ids[node]} [label=\"{node!r}\"]")
        else:
            lines.append(f"  {ids[node]}")
    for a, b in edges:
        lines.append(f"  {ids[a]} -> {ids[b]}")

    lines.append("}")
    return "\n".join(lines)
