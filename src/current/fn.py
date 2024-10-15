from current.var import Var

class Fn(Var):
    def __init__(self, f, *args, name="fn"):
        self.f = f
        self.args = args
        super().__init__(self._evaluate(), name=name)
        for arg in args:
            if isinstance(arg, Var):
                arg._subscribe(self)

    def refresh(self):
        self.update(self._evaluate())

    def _evaluate(self):
        arg_values = []
        for arg in self.args:
            if isinstance(arg, Var):
                arg_values.append(arg.get())
            else:
                arg_values.append(arg)
        return self.f(*arg_values)
