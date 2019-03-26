# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: 导出本地chtterbot语料
'''
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  #解决跨模块导入包的一种方案
from core.MyRobot import Bot
'''
如果一个已经训练好的chatbot，你想取出它的语料，用于别的chatbot构建，可以这么做
'''

# 把语料导出到json文件中
if __name__ == '__main__':
    for i in range(1,6):
        bot=Bot.chattbot("XbtCorpus%s"%i)
        bot.trainer.export_for_training('./my_export.json%s'%i)