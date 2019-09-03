import tqdm as tq
from functools import wraps
import sys

def close_and_leave(f):
    @wraps(f)
    def _f(self, *args, **wargs):
        if not hasattr(self, 'entered_close'):
            self.entered_close = True
            if sys.stdout != sys.__stdout__ and self.leave:
                string = self.__repr__()
                sys.stdout.f.write(string+'\n')
                sys.stdout.f.flush()
            f(self, *args, **wargs)
    return _f
tq.tqdm.close = close_and_leave(tq.tqdm.close)


# class tqdm(tq.tqdm):
#     def close(self):
#         if not hasattr(self, 'entered_close'):
#             self.entered_close = True
#             if sys.stdout != sys.__stdout__ and self.leave:
#                 string = self.__repr__()
#                 sys.stdout.sf.write(string+'\n')
#                 sys.stdout.f.flush()
#             super(tqdm,self).close()
