#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1服务端启动文件，
'''

import os,sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)  #解决跨模块导入包的一种方案

import socket
import struct

from concurrent.futures import ThreadPoolExecutor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from settings import setting
from core.process import RobotProces

class XbtRobotServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    request_queue_size = 5

    def __init__(self,server_address,max_num_threads,bind_and_activate=True):
        self.server_address=server_address
        self.socket=socket.socket(self.address_family,
                                  self.socket_type)
        self.pool = ThreadPoolExecutor(max_num_threads)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise
    # @classmethod
    # def run_sever(cls):
    #     obj=cls(setting.SERVER_ADDRESS,setting.MAX_NUM_THREADS)
    #     return obj

    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind(self.server_address)
        self.server_address=self.socket.getsockname()

    def server_activate(self):
        self.socket.listen(self.request_queue_size)
        print('starting......')

    def server_close(self):
        self.socket.close()

    def get_request(self):
        return self.socket.accept()

    def close_request(self,request):
        request.close()

    @staticmethod
    def get_response(question):
        bot = RobotProces(question)
        bot.think()
        return bot.response.encode('utf-8')


    def communication(self,conn):
        while True:
            try:
                question= self.recvinfo(conn).decode('utf-8')
                answer = self.get_response(question)
                self.sendinfo(answer,conn)
            except Exception as e:
                break

    def run_connect(self):
            while True:
                conn, self.client_addr = self.get_request()
                print('from client ', self.client_addr)
                self.pool.submit(self.communication,conn)

    def sendinfo(self,response,conn):
        send_total_size = len(response)
        head_struct = struct.pack('i', send_total_size)
        conn.send(head_struct)
        conn.send(response)

    def recvinfo(self,conn):
        obj = conn.recv(4)
        recv_total_size=struct.unpack('i',obj)[0]
        recv_size = 0
        recv_data = b''
        while recv_size < recv_total_size:
            res = conn.recv(12)
            recv_size +=len(res)
            recv_data +=res
        return recv_data












if __name__ == '__main__':
    tcpserver1 = XbtRobotServer(('192.168.1.106',8024),3)
    tcpserver1.run_connect()