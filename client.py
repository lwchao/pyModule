#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   client.py
@Version :   1.0
@Author  :   liuwenchao
@Contact :   liuwenchao@qianxin.com
@Time    :   2020/12/06 00:13:04
'''

import time
import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 1401))

    while True:
        msg = "hello,my name is ChenYan!"
        slen = '%08d' % (len(msg))
        s.sendall(slen)
        s.sendall(msg)
        msg = s.recv(1024)
        print(msg)
        time.sleep(5)
    

if __name__ == "__main__":
    main()
