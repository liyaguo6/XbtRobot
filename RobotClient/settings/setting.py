# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1 客户端配置文件信息
'''



import os,sys


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)


### 掺用文件术语的调用
SPEAK_PATH = os.path.join(BASE_DIR,"database\\vad_speak\\")
SPEACK_FILE = os.path.join(BASE_DIR,"database\\speak\\test.wav")
SPEACK_TERMS_FILE = os.path.join(BASE_DIR,"terms\\speak_term\\speak_error.wav")
LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\1kXF.wav")
Initial_LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\initial_test.wav")  # 语音初始化文件
LISTEN_TERMS_FILE =os.path.join(BASE_DIR,"terms\\listen_term\\listen_error.wav")
START_TERNS_DIR = os.path.join(BASE_DIR,'terms\\start_term')
BYE_TERMS_FILE = os.path.join(BASE_DIR,"terms\\bye_term\\bye.wav")
INTERRUPT_TERMS_FILE = os.path.join(BASE_DIR,"terms\\interrupt\\inp.wav")
PLAY_MEDIA = r"D:/ffmpeg/bin/ffplay"
TRANSVERTER=r"D:/ffmpeg/bin/ffmpeg"
msc_x64_FILE= os.path.join(BASE_DIR,"database\\dll_file\\msc_x64.dll") # 动态链接库路径






#百度token配置参数
Grant_type = "client_credentials"
Client_id = "6vnvj2pvAFfbUVcXuUoW4YeD"
Client_secret = "Vm7fHywZubDqk2oNKNG9OpF5QTNtL5hG"


#讯飞配置
LOGIN_PARAMS = b"appid = 5b559fed, work_dir = ."    # 语音识别登录参数，apppid一定要和你的下载SDK对应
APPID = "5b574774"
ASR_API_KEY = "771cb83d1fd6a30a5bba996e4650ecb3"
TTS_API_KEY = "2ae7d8d0cdddeb17aaa6864378dddab2"
URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"       # 得到语音文件以.wav格式写入
HEAD_PARAM = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"


#文本分类器配置参数
STOPWORDS = os.path.join(BASE_DIR,'database\\features\\stop_words.pkl')
TRAIN_FEATURES_WORDS = os.path.join(BASE_DIR,'database\\features\\train_features_words.pkl')
TRAIN_FEATURES = os.path.join(BASE_DIR,'database\\features\\train_features.pkl')



#链接服务端的IP和端口
SERVER_ADDRESS = ('192.168.1.106',8024)

#关键字
BYEKEYWODS= r'(再见|goodbye|byebye|拜拜|退出|再会|待会见)'
ORDERKEYWORDS = r'(是的|继续说|我想听|接着说)'
ORDERKEYWORDS1 = r'(不要说了|不想听|不用说了)'


