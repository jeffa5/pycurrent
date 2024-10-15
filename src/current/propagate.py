import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


def propagate(*args):
    logger.debug("Building dependency graph")
    changed_args = [a for a in args if a._changed()]
    for arg in changed_args:
        arg._seen_change()
    g = set()
    deps = defaultdict(set)
    q = deque(changed_args)
    while q:
        node = q.popleft()
        if node in g:
            logger.debug("Node %r already seen", node.name)
            continue

        g.add(node)

        for reader in node.readers:
            logger.debug("Adding dependency from %r to %r", reader.name, node.name)
            deps[reader].add(node)
            q.append(reader)

    logger.debug("Built dependency graph")
    logger.debug("Doing propagation")

    # node and whether to refresh it
    q = deque([(c, True) for c in changed_args])
    while q:
        node, refresh = q.popleft()
        if node not in g:
            logger.debug("Skipping %r as already processed", node.name)
            # already processed
            continue
        if deps[node]:
            # not ready yet
            logger.debug("Skipping %r as not all depencies are satisfied", node.name)
            if len(q) == 0:
                raise Exception("re-adding element would lead to infinite cycle")
            q.append((node, refresh))
            continue


        if refresh:
            logger.debug("Refreshing %r", node.name)
            g.remove(node)
            node.refresh()
        else:
            logger.debug("Not refreshing %r", node.name)

        for reader in node.readers:
            if reader in deps:
                deps[reader].remove(node)
            q.append((reader, node._changed()))

    logger.debug("Done propagation")
