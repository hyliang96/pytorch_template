import errno, os

class Max(object):
    def __init__(self):
        pass
    def add(self, key, value):
        if (not hasattr(self,'value')) or self.value < value:
            self.key = key
            self.value = value

def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

