
import logging
from chatterbot import ChatBot
"""
反馈式的聊天机器人，会根据你的反馈进行学习
"""

# 把下面这行前的注释去掉，可以把一些信息写入日志中
# logging.basicConfig(level=logging.INFO)

# # 创建一个聊天机器人
# bot = ChatBot(
#     'Feedback Learning Bot',
#     storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
#     logic_adapters=[
#         'chatterbot.logic.BestMatch'
#     ],
#     input_adapter='chatterbot.input.TerminalAdapter',#命令行端
#     output_adapter='chatterbot.output.TerminalAdapter'
# )


bot = ChatBot("Terminal",
              storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
              logic_adapters=[
                  {'import_path': "chatterbot.logic.BestMatch"}, # BestMatch 逻辑adater根据与输入语句最接近的匹配的已知响应返回响应

              ],

              input_adapter="chatterbot.input.TerminalAdapter",
              output_adapter="chatterbot.output.TerminalAdapter",
              database_uri="mongodb://localhost:27017/",    # 设置你的数据库所在的地址端口号
              database="xbt_test",       #这是你的数据库名称,如果没有,首次他会自动创建
              trainer='chatterbot.trainers.ListTrainer'
              )

#
bot.train([
        "这是指南针科创园领导来视察。",
        "欢迎领导莅临指导",
        "这是指南针科创园的领导马总",
            "领导辛苦了",
    ])

#
DEFAULT_SESSION_ID = bot.storage.create_conversation()
print(DEFAULT_SESSION_ID)

def get_feedback():
    from chatterbot.utils import input_function
    # text = input_function()
    ret = input("错误输入0正确1>>")
    if "1" == ret:
        return True
    elif "0" == ret:
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()

#
# print('Type something to begin...')
#
# # 每次用户有输入内容，这个循环就会开始执行
# while True:
#     try:
#         input_statement = bot.input.process_input_statement()
#         # input_statement = input("输入问题>>>")
#         statement, response = bot.generate_response(input_statement, DEFAULT_SESSION_ID)
#         # response = bot.generate_response(input_statement)
#         # response = bot.get_response(input_statement,DEFAULT_SESSION_ID)
#         bot.output.process_response(response)
#         print('\n Is "{}" this a coherent response to "{}"? \n'.format(response, input_statement))
#         if get_feedback():
#             print("please input the correct one")
#
#             response1 = bot.input.process_input_statement()
#
#             bot.learn_response(response1, input_statement)
#
#             bot.storage.add_to_conversation(DEFAULT_SESSION_ID, statement, response1)
#
#             print("Responses added to bot!")
#
#         bot.output.process_response(response)
#         # # 更新chatbot的历史聊天数据
#
#
#
#     # 直到按ctrl-c 或者 ctrl-d 才会退出
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break
