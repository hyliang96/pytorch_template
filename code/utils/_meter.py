import torchnet.meter as meter
from functools import wraps
import torch

def detach_input(f):
    @wraps(f)
    def _f(*args, **wargs):
        args = [arg.detach() if type(arg)==torch.Tensor else arg for arg in args ]
        wargs = { key : arg.detach() if type(arg)==torch.Tensor else arg for key,arg in wargs.items() }
        return f(*args, **wargs)
    return _f

def change_value1(f):
    @wraps(f)
    def _f(*args, **wargs):
        value = f(*args, **wargs)
        return value[0]
    return _f

def change_value2(f):
    @wraps(f)
    def _f(*args, **wargs):
        value = f(*args, **wargs)
        if type(value)==list and len(value)==1:
            return value[0]
        else:
            return value
    return _f

meter.ClassErrorMeter.add = detach_input(meter.ClassErrorMeter.add)
meter.ClassErrorMeter.value = change_value2(meter.ClassErrorMeter.value)

meter.AverageValueMeter.add = detach_input(meter.AverageValueMeter.add)
meter.AverageValueMeter.value = change_value1(meter.AverageValueMeter.value)

meter.ConfusionMeter.add = detach_input(meter.ConfusionMeter.add)



# def detach_input(f):
#     @wraps(f)
#     def _f(*args, **wargs):
#         args = [arg.detach() if type(arg)==torch.Tensor else arg for arg in args ]
#         wargs = { key : arg.detach() if type(arg)==torch.Tensor else arg for key,arg in wargs.items() }
#         return f(*args, **wargs)
#     return _f

# class ClassErrorMeter(meter.ClassErrorMeter):
#     @detach_input
#     def add(self, *args, **wargs):
#         return super().add(*args, **wargs)

#     def value(self, *args, **wargs):
#         value = super().value(*args, **wargs)
#         if type(value)==list and len(value)==1:
#             return value[0]
#         else:
#             return value

# class AverageValueMeter(meter.AverageValueMeter):s
#     @detach_input
#     def add(self, *args, **wargs):
#         return super().add(*args, **wargs)

#     def value(self):
#         return super().value()[0]
#     # 变量 std

# class ConfusionMeter(meter.ConfusionMeter):
#     @detach_input
#     def add(self, *args, **wargs):
#         return super().add(*args, **wargs)
