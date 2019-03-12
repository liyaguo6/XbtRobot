import os,sys


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

SPEAK_PATH = os.path.join(BASE_DIR,"database\\vad_speak\\")
SPEACK_FILE = os.path.join(BASE_DIR,"database\\speak\\test.wav")
SPEACK_TERMS_FILE = os.path.join(BASE_DIR,"terms\\speak_term\\speak_error.wav")

LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\1kXF.wav")
LISTEN_TERMS_FILE =os.path.join(BASE_DIR,"terms\\listen_term\\listen_error.wav")
CONTINUE_TERMS_FILE=os.path.join(BASE_DIR,"terms\\continue_term\\continue.wav")
START_TERNS_DIR = os.path.join(BASE_DIR,'terms\\start_term')
BYE_TERMS_FILE = os.path.join(BASE_DIR,"terms\\bye_term\\bye.wav")
PLAY_MEDIA = r"D:/ffmpeg/bin/ffplay"
TRANSVERTER=r"D:/ffmpeg/bin/ffmpeg"

SDK_FILE =r"E:\Windows_aisound_exp1208_aitalk_exp1208_awaken_exp1208_iat1208_tts_online1208_5b559fed\bin\msc_x64.dll"

NAME = "XbtRobot"
Storage_Adapter='chatterbot.storage.MongoDatabaseAdapter'
THRESHOLD = 0.65  #本地数据库识别可信度阈值
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

#百度token配置参数
Grant_type = "client_credentials"
Client_id = "6vnvj2pvAFfbUVcXuUoW4YeD"
Client_secret = "Vm7fHywZubDqk2oNKNG9OpF5QTNtL5hG"

#文本分类器配置参数
STOPWORDS = os.path.join(BASE_DIR,'database\\features\\stop_words.pkl')
TRAIN_FEATURES_WORDS = os.path.join(BASE_DIR,'database\\features\\train_features_words.pkl')
TRAIN_FEATURES = os.path.join(BASE_DIR,'database\\features\\train_features.pkl')

#连接未能回答问题的数据库
IP = '127.0.0.1'
PORT =27017
DB ="unquestion"
TABLE='mtest'


