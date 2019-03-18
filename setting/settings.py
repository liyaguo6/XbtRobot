import os,sys


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

SPEAK_PATH = os.path.join(BASE_DIR,"database\\vad_speak\\")
SPEACK_FILE = os.path.join(BASE_DIR,"database\\speak\\test.wav")
SPEACK_TERMS_FILE = os.path.join(BASE_DIR,"terms\\speak_term\\speak_error.wav")
LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\1kXF.wav")
Initial_LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\initial_test.wav")  # 语音初始化文件
LISTEN_TERMS_FILE =os.path.join(BASE_DIR,"terms\\listen_term\\listen_error.wav")
START_TERNS_DIR = os.path.join(BASE_DIR,'terms\\start_term')
BYE_TERMS_FILE = os.path.join(BASE_DIR,"terms\\bye_term\\bye.wav")
PLAY_MEDIA = r"D:/ffmpeg/bin/ffplay"
TRANSVERTER=r"D:/ffmpeg/bin/ffmpeg"
msc_x64_FILE= os.path.join(BASE_DIR,"database\\dll_file\\msc_x64.dll") # 动态链接库路径

long_limit = 150 # 切割答案长度门限
first_len =  50 # 播放语音第一段长度

NAME = "XbtRobot"
Storage_Adapter='chatterbot.storage.MongoDatabaseAdapter'
THRESHOLD = 0.7  #本地数据库识别可信度阈值
Logic_Adapters=[
              {'import_path': "chatterbot.logic.BestMatch"},
                {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',  # LowConfidenceAdapter当高信度响应未知时，返回具有高置信度的默认响应。
                'threshold': THRESHOLD,
                'defa'
                'ult_response': 'False'
                },
          ]
Filters = [
              'chatterbot.filters.RepetitiveResponseFilter'  # 这是一个滤波器,它的作用是滤掉重复的回答
          ]

Input_Adapter = "chatterbot.input.VariableInputTypeAdapter"
Output_Adapter = "chatterbot.output.OutputAdapter"
Database_Uri = "mongodb://localhost:27017/"  # 设置你的数据库所在的地址端口号
READ_ONLY = True
Train_Features_Words_File = os.path.join(BASE_DIR,"classifier\\database\\features\\train_features_words.pkl")
Train_Features_File = os.path.join(BASE_DIR,"classifier\\database\\features\\train_features.pkl")




Tulin_API_KEY = "164391ebc59c48a88c7c4cc41682e5a3"
SYNO_FILES=os.path.join(BASE_DIR,'synom\\new_synomys.json')

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

#连接未能回答问题的数据库
IP = '127.0.0.1'
PORT =27017
DB ="unquestion"
TABLE='mtest'


