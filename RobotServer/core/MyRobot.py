# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: chatterbot对象的封装
'''
from chatterbot import ChatBot
from settings import setting


class Bot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # print(kwargs)
        # self.name =name

    @classmethod
    def chattbot(cls, database):
        chat = cls(setting.NAME,
                   storage_adapter=setting.Storage_Adapter,
                   logic_adapters=setting.Logic_Adapters,
                   filters=setting.Filters,
                   input_adapter=setting.Input_Adapter,
                   output_adapter=setting.Output_Adapter,
                   database=database,
                   read_only=setting.READ_ONLY
                   )
        return chat

# if __name__ == '__main__':
    # bot = Bot.chattbot('XbtCorpus1')
    # bot.get_response()
# bot = XbtBot("Terminal",
#               storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
#               logic_adapters=[
#                   {'import_path': "chatterbot.logic.BestMatch"}, # BestMatch 逻辑adater根据与输入语句最接近的匹配的已知响应返回响应
#                   {
#                       'import_path': 'chatterbot.logic.LowConfidenceAdapter',# LowConfidenceAdapter当高信度响应未知时，返回具有高置信度的默认响应。
#                       'threshold': settings.THRESHOLD,
#                       'defa'
#                       'ult_response': 'False'
#                   },
#               ],
#               filters=[
#                   'chatterbot.filters.RepetitiveResponseFilter' #这是一个滤波器,它的作用是滤掉重复的回答
#               ],
#
#               input_adapter="chatterbot.input.VariableInputTypeAdapter",
#               output_adapter="chatterbot.output.OutputAdapter",
#               database_uri="mongodb://localhost:27017/",    # 设置你的数据库所在的地址端口号
#               database="xbtgover",       #这是你的数据库名称,如果没有,首次他会自动创建
#               read_only=True,
#               )



