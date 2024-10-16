from current.var import Var
from current.utils import List
import logging

logger = logging.getLogger(__name__)

class Fn(Var):
    def __init__(self, f, *args, name="fn", **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        super().__init__(None, name=name)
        self.refresh()
        for arg in args:
            if isinstance(arg, Var):
                arg._subscribe(self)
        for kwarg in kwargs.values():
            if isinstance(kwarg, Var):
                kwarg._subscribe(self)

    def refresh(self):
        val = self._evaluate()
        self.update(val)

    def _evaluate(self):
        logger.debug("Evaluating fn %r", self.name)
        arg_values = []
        for arg in self.args:
            if isinstance(arg, Var):
                arg_values.append(arg.get())
            else:
                arg_values.append(arg)
        kwarg_values = {}
        for k, v in self.kwargs.items():
            if isinstance(v, Var):
                kwarg_values[k] = v.get()
            else:
                kwarg_values[k] = v

        val = self.f(*arg_values, **kwarg_values)

        if isinstance(val, List):
            for v in val:
                if isinstance(v, Var):
                    self._subscribe(v)

        return val
