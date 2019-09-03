import torch
from functools import wraps

def remove_module(f):
    @wraps(f)
    def _f(self, *args, **wargs):
        if hasattr(self, 'module'):
            return f(self.module,  *args,**wargs)
        else:
            return f(self,  *args,**wargs)
    return _f
torch.nn.Module.state_dict = remove_module(torch.nn.Module.state_dict)
