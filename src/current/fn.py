from current.var import Var


class Fn(Var):
    def __init__(self, f, *args, name="fn"):
        super().__init__(None, name=name)
        self.f = f
        self.args = args
        for arg in args:
            if isinstance(arg, Var):
                arg._subscribe(self)
        self.initialized = False

    def with_args(self, *args):
        for arg in self.args:
            if isinstance(arg, Var):
                arg._unsubscribe(self)
        self.args = args
        for arg in args:
            if isinstance(arg, Var):
                arg._subscribe(self)

    def get(self):
        if not self.initialized:
            self.refresh()
            self.initialized = True
        return self.value

    def refresh(self):
        arg_values = []
        for arg in self.args:
            if isinstance(arg, Var):
                arg_values.append(arg.get())
            else:
                arg_values.append(arg)
        self.value = self.f(*arg_values)

