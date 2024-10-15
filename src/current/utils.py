from collections import UserList
import current


def flatten(l):
    """
    Convert a list of var-likes to a var-like of a list
    """
    return current.Fn(lambda xs: [x.get() for x in xs], l)

class List(UserList):
    """
    An annotator that a function can unwrap this and add dependencies from internal items.
    """
    def __init__(self, *args):
        super().__init__(*args)
