from current.var import Var
from current.utils import List

class Fn(Var):
    def __init__(self, f, *args, name="fn"):
        self.f = f
        self.args = args
        super().__init__(None, name=name)
        self.refresh()
        for arg in args:
            if isinstance(arg, Var):
                arg._subscribe(self)

    def refresh(self):
        val = self._evaluate()
        self.update(val)

    def _evaluate(self):
        arg_values = []
        for arg in self.args:
            if isinstance(arg, Var):
                arg_values.append(arg.get())
            else:
                arg_values.append(arg)

        val = self.f(*arg_values)

        if isinstance(val, List):
            for v in val:
                if isinstance(v, Var):
                    self._subscribe(v)

        return val
