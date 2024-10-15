from collections import deque


def graph(*args):
    seen = set()
    q = deque(args)
    lines = []
    lines.append("digraph {")
    lines.append("rankdir=LR")
    while q:
        node = q.popleft()
        if node in seen:
            continue

        for reader in node.readers:
            lines.append(f"{node.name} -> {reader.name}")
            q.append(reader)
    lines.append("}")
    return "\n".join(lines)
