import argparse
def _print(self):
    return '\n'.join([arg+' : '+str(getattr(self, arg)) for arg in vars(self)])
argparse.Namespace.__str__ = _print

import torch
def _optimizer_to(self, device):
    for state in self.state.values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.to(device)
torch.optim.Optimizer.to = _optimizer_to