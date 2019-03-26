# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1服务端启动文件
'''

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  #解决跨模块导入包的一种方案
from main.main import XbtRobotServer
if __name__ == '__main__':
    tcpserver1 = XbtRobotServer(('192.168.1.106',8024),3)
    tcpserver1.run_connect()