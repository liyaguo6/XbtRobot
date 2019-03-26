# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1客户端启动文件
'''


import os, time,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  #解决跨模块导入包的一种方案
from main.main import XbtBot
if __name__ == '__main__':
    start = XbtBot()
    start.run()