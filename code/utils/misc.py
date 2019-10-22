import errno, os



class Best(object):
    def __init__(self, key, reverse=False):
        self.datas = {}
        self.key = key
        self._id = 0
        self.best_id = 0
        self.reverse = reverse


    def add(self, data_id, data_dict):
        self.datas[data_id] = data_dict
        value = data_dict[self.key]
        if (not hasattr(self,'best_value')) or \
           ( (not self.reverse) and self.best_value < value ) or \
           (      self.reverse  and self.best_value > value ):
            self.best_id = data_id
            self.best_value = value

    def data(self):
        return {'best_'+key: value for key, value in self.datas[self.best_id].items()}

    def value(self):
        return self.best_value

    def id(self):
        return self.best_id


class Min(Best):
    def __init__(self, key):
        super().__init__(key, reverse=True)

class Max(Best):
    def __init__(self, key):
        super().__init__(key, reverse=False)
# class Max(object):
#     def __init__(self):
#         pass
#     def add(self, key, value):
#         if (not hasattr(self,'value')) or self.value < value:
#             self.key = key
#             self.value = value

def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

