import cv2,os
from chatterbot import ChatBot
import pandas as pd
# from core.speakout import tts_main
from chatterbot.trainers import ChatterBotCorpusTrainer
# tts_main("请讲")

#
# df = pd.read_csv(r'D:\MyProj\XbtChatterbot2018\xbtRobot1.1\trainning\gover2.csv', header=0 \
#                  ,encoding='gbk',usecols=['labels','origques','answer'])
# for index,rows in df.head().iterrows():
#     print(rows)

# print(os.listdir(r'D:\MyProj\XbtChatterbot2018\xbtRobot1.1\trainning\croups'))
# print(os.path)
# kwargs ={
#     'AS':12,
#     'DS':34
# }
# def dict_test(**kwargs):
#     print(kwargs)
# dict_test(**kwargs)
path = r'D:\MyProj\XbtChatterbot2018\xbtRobot1.1\trainning\croups'
dirs = os.listdir(path)
import json
# for name in dirs:
#     with open(os.path.join(path,name),'r') as f:
#         load_dict = json.load(f)
#         print(len(load_dict['conversations']))


bot = ChatBot("XbtRobot",
          storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
          logic_adapters=[
              {'import_path': "chatterbot.logic.BestMatch"},
          ],
          filters=[
              'chatterbot.filters.RepetitiveResponseFilter'
          ],
          # trainer='chatterbot.trainers.ListTrainer',
          input_adapter="chatterbot.input.VariableInputTypeAdapter",
          output_adapter="chatterbot.output.OutputAdapter",
          database_uri="mongodb://localhost:27017/",
          database="XbtCorpus4",
          read_only=True,
          # trainer='chatterbot.trainers.ListTrainer'
          )
bot.set_trainer(ChatterBotCorpusTrainer)

bot.trainer.export_for_training('./XbtCorpus4.json')
with open('./XbtCorpus4.json','r') as f:
    data=json.load(f)['conversations']
    que,ans = list(zip(*data))
    df=pd.DataFrame({'ques':pd.Series(que),'answ':pd.Series(ans)})
    df.to_csv('./XbtCorpus4.csv',encoding='gbk')