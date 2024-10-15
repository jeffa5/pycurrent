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

    def _subscribe(self, other):
        self.readers.add(other)

    def _unsubscribe(self, other):
        self.readers.remove(other)

