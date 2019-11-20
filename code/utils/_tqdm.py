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



# from tqdm._utils import _environ_cols_wrapper
# def set_dynamic_ncols_true(f):
#     @wraps(f)
#     def _f(self, *args, ncols=None, **wargs):
#         f(self, *args, ncols=ncols, **wargs)
#         self.ncols = ncols or _environ_cols_wrapper()(self.fp)
#     return _f
# tq.tqdm.__init__ = set_dynamic_ncols_true(tq.tqdm.__init__)

def set_dynamic_ncols_true(f):
    @wraps(f)
    def _f(self, *args, dynamic_ncols=True, **wargs):
        f(self, *args, dynamic_ncols=dynamic_ncols, **wargs)
    return _f
tq.tqdm.__init__ = set_dynamic_ncols_true(tq.tqdm.__init__)


# def clear_when_update(f):
#     @wraps(f)
#     def _f(self, *args, **wargs):
#         ncols=self.dynamic_ncols(self.fp) if self.dynamic_ncols else self.ncols
#         if ncols!= self.ncols:
#             self.clear()
#         f(self, *args, **wargs)
#         self.ncols = ncols
#     return _f
# tq.tqdm.update = clear_when_update(tq.tqdm.update)


# class tqdm(tq.tqdm):
#     def close(self):
#         if not hasattr(self, 'entered_close'):
#             self.entered_close = True
#             if sys.stdout != sys.__stdout__ and self.leave:
#                 string = self.__repr__()
#                 sys.stdout.sf.write(string+'\n')
#                 sys.stdout.f.flush()
#             super(tqdm,self).close()
