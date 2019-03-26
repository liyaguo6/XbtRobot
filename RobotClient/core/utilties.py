# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: 常用接口函数
'''
import os
import re
import random
from settings import setting

def random_start_terms():
    """
    随机固定用语
    :return:
    """
    start_dir = setting.START_TERNS_DIR
    file_name_list = os.listdir(start_dir)
    file_name = random.sample(file_name_list,1)[0]
    start_term_path = os.path.join(start_dir,file_name)
    return start_term_path

def split_words(response):
    """
    对于过长（超过50个字符）的回答，分割成两部分
    :param response: 检测的问答
    :return:
    """
    response_list= re.split(r',|，|。|？|；|！', response)
    response1 =""
    for index,value in enumerate(response_list):
        if len(response1) <30:
            if index ==0:
                response1 = value
            else:
                response1 =response1+','+value
        else:
            response2 = ''.join(response_list[index:])
            break
    return response1,response2







if __name__ == '__main__':
    # random_start_terms()
    response = '我是来自新巴特的Oh boy，我是巧妙的工程师们造出来的，我现在还是个宝宝哦。'