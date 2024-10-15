class Var:
    def __init__(self, val, name="var"):
        self.name = name
        self.value = val
        self.readers = set()
        self.modified = False

    def update(self, val):
        """
        Update the value stored in this variable.
        """
        if self.value == val:
            self.modified = False
            return
        self.modified = True
        self.value = val

    def refresh(self):
        """
        Refresh the value in this variable.
        """


    def get(self):
        """
        Return the value stored in this variable.
        """
        return self.value

    def _changed(self) -> bool:
        return self.modified

    def _seen_change(self):
        self.modified = False

    def _subscribe(self, other):
        self.readers.add(other)

    def _unsubscribe(self, other):
        self.readers.remove(other)

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, value={self.value}, modified={self.modified})"
