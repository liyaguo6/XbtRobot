# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1客户端功能封装
'''

import socket
import struct
import json
import os


class Client:
    address_family=socket.AF_INET
    socket_type=socket.SOCK_STREAM

    def __init__(self,server_address,connect=True):
        self.server_address=server_address
        self.socket=socket.socket(self.address_family,
                                  self.socket_type)

        if connect:
            try:
                self.client_connect()
            except:
                self.client_close()
                raise

    def client_connect(self):
        """
        链接服务端
        :return:
        """
        self.socket.connect(self.server_address)

    def client_close(self):
        self.socket.close()

    def send_recv(self,words):
        """
        收发消息的调用
        :param words: 需要发送的消息文字
        :return:
        """
        inp_bytes = words.encode('utf-8')
        self.sendinfo(inp_bytes)
        self.response = self.recvinfo()
        return self.response.decode('utf-8')



    def sendinfo(self,inp_bytes):
        """
        发送客户端消息
        :param inp_bytes:
        :return:
        """
        send_total_size = len(inp_bytes)
        head_struct = struct.pack('i', send_total_size)
        self.socket.send(head_struct)
        self.socket.send(inp_bytes)

    def recvinfo(self):
        """
        接受服务端消息
        :return:
        """
        obj = self.socket.recv(4)
        recv_total_size=struct.unpack('i',obj)[0]
        recv_size = 0
        recv_data = b''
        while recv_size < recv_total_size:
            res1 = self.socket.recv(5)
            recv_size +=len(res1)
            recv_data +=res1
        return recv_data






if __name__ == '__main__':

    client=Client(('127.0.0.1',8092))
    client.run()
