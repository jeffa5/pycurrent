class Var:
    def __init__(self, val, name="var"):
        self.name = name
        self.value = val
        self.readers = set()

    def update(self, val):
        self.value = val

    def refresh(self):
        pass

    def get(self):
        return self.value

    def _changed(self) -> bool:
        return True

    def _seen_change(self):
        pass

    def _subscribe(self, other):
        self.readers.add(other)

    def _unsubscribe(self, other):
        self.readers.remove(other)

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, value={self.value})"


class CachedVar(Var):
    def __init__(self, val, name="cvar"):
        super().__init__(val, name=name)
        self.modified = False

    def update(self, val):
        if val == self.value:
            self.modified = False
            return
        self.modified = True
        super().update(val)

    def _changed(self) -> bool:
        return self.modified

    def _seen_change(self):
        self.modified = False

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, value={self.value}, modified={self.modified})"
