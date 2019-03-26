# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: 原始文本信息处理
'''

import pandas as pd
import random
process_data={}
def get_data(path_raw,path_oth,save_path=None):
    save_path = './database/processed_data.csv'
    df = pd.read_csv(path_raw,header=0,encoding='gbk',error_bad_lines=True)
    for i in range(1,6):
        cdf = df[df['labels']==i]
        tmp_list=[]
        for j in range(1,6):
            ques = 'question%s'%j
            tmp_list.extend(list(cdf[ques][cdf[ques].notnull()]))
        process_data[i]=tmp_list

    df_oth = pd.read_csv(path_oth,header=None,encoding='gbk',error_bad_lines=True,names=['question'])
    process_data[0] = random.sample(list(df_oth.loc[:,'question']),40000)
    return process_data

# if __name__ == '__main__':
#     ret=get_data()
#     for index,values in ret.items():
#         print('class%s has %s samples'%(index,len(values)))