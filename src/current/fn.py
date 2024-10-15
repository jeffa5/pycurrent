from current.var import Var, CachedVar

class BaseFn:
    def __init__(self, f, *args):
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
        self.update(self.f(*arg_values))


class Fn(BaseFn, Var):
    def __init__(self, f, *args, name="fn"):
        Var.__init__(self, None, name=name)
        BaseFn.__init__(self, f, *args)


class CachedFn(BaseFn, CachedVar):
    def __init__(self, f, *args, name="cfn"):
        CachedVar.__init__(self, None, name=name)
        BaseFn.__init__(self, f, *args)
