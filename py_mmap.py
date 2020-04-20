#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test.py
@Version :   1.0
@Author  :   liuwenchao
@Time    :   2020/04/20 11:18:37
'''

from fcntl import flock, LOCK_EX, LOCK_UN

import pickle
import mmap
import os, stat

filenameFormat = "/tmp/test%s"
CACHESIZE = 1024 * 1024

def save_mem(obj, base):
    filename = filenameFormat % base
    mem = pickle.dumps(obj)
    lenth = len(mem)

    with open(filename, 'wb+') as fd:
        flock(fd, LOCK_EX)
        fd.write(mem)
        fd.write(b'0' * (CACHESIZE - lenth))
        flock(fd, LOCK_UN)
        os.chmod(filename, stat.S_IRWXG)

def refresh_mem(obj, base):
    filename = filenameFormat % base
    mem = pickle.dumps(obj)
    lenth = len(mem)

    with open(filename, 'a+') as fd:
        flock(fd, LOCK_EX)
        mshare = mmap.mmap(fd.fileno(), CACHESIZE)
        mshare[:] = "%s%s" % (mem, '\0' * (CACHESIZE - lenth))
        mshare.flush()
        mshare.close()
        flock(fd, LOCK_UN)
    
def get_mem(base):
    filename = filenameFormat % base
    with open(filename, 'r+') as fd:
        flock(fd, LOCK_EX)
        mshare = mmap.mmap(fd.fileno(), CACHESIZE)
        flock(fd, LOCK_UN)

    mobj = pickle.loads(mshare[:])
    mshare.close()
    return mobj

def main():
    obj = {"a":1, "b":2}
    save_mem(obj, 'saveOne')
    print get_mem('saveOne')


if __name__ == "__main__":
    main()
