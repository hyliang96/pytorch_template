import argparse
def _print(self):
    return '\n'.join([arg+' : '+str(getattr(self, arg)) for arg in vars(self)])
argparse.Namespace.__str__ = _print


def _dict(self):
    return {key:str(value) for key,value in vars(self).items()}
argparse.Namespace.dict = _dict

import torch
def _optimizer_to(self, device):
    for state in self.state.values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.to(device)
torch.optim.Optimizer.to = _optimizer_to
