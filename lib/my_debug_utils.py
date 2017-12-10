import time

def timeof(f):
    def wrapp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print(time.time()-t)
        return res
    return wrapp