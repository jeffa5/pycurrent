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

    q = deque(changed_args)
    while q:
        node = q.popleft()
        if node not in g:
            logger.debug("Skipping %r as already processed", node.name)
            # already processed
            continue
        if deps[node]:
            # not ready yet
            logger.debug("Skipping %r as not all depencies are satisfied", node.name)
            q.append(node)
            continue

        logger.debug("Refreshing %r", node.name)
        g.remove(node)

        node.refresh()

        for reader in node.readers:
            if reader in deps:
                deps[reader].remove(node)
            q.append(reader)

    logger.debug("Done propagation")
