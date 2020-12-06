#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   server.py
@Version :   1.0
@Author  :   liuwenchao
@Contact :   liuwenchao@qianxin.com
@Time    :   2020/12/06 00:07:12
'''

from socket import error
import sys
import threading
import SocketServer

client_array = {}
thread_lock = threading.Lock()

class BaseServer(SocketServer.BaseRequestHandler):
    def setup(self):
        self.event = threading.Event()
        with thread_lock:
            client_array[self.client_address] = self.request
        print("setup recv address: {}".format(self.client_address))
    
    def rrecv_with_len(self):
        conn = self.request
        try:
            d = conn.recv(8)
            if not d:
                return ''
            dlen = int(d)
            print("dlen: {}".format(dlen))
            data = conn.recv(dlen)
            if not data:
                return ''
            return data
        except Exception as error:
            print("Error: {}".format(error))
            return ''

    def rrecv(self):
        data_array = []
        conn = self.request
        while(True):
            try:
                msg = conn.recv(5)
                print(msg)
                if len(msg) < 5:
                    data_array.append(msg)
                    break
                data_array.append(msg)
            except Exception as err:
                print("error: {}".format(err))
                break
        print(data_array)
        return ''.join(data_array)


    def handle(self):
        while not self.event.is_set():
            msg = self.rrecv_with_len()
            if not msg:
                break

            print("port:{} msg: {}".format(self.client_address[1], msg))
            self.request.sendall("success")

    def finish(self):
        self.event.set()
        with thread_lock:
            client_array.pop(self.client_address, None)

        self.request.close()
        print("finish conn:{} close".format(self.client_address[1]))

import signal

def main():
    
    s = SocketServer.ThreadingTCPServer(("127.0.0.1", 1401), BaseServer)
    s.allow_reuse_address = True
    # s.server_bind()
    # s.server_activate()
    s.serve_forever()
    
    # s.shutdown() #告诉serve_forever循环停止。
    # s.server_close()

if __name__ == "__main__":
    main()
