# -*- coding: utf-8 -*-
## 语音合成后，直接读出合成的音频文件
import requests
import time
import hashlib
import base64
import pyaudio

from settings import setting

URL =setting.URL
AUE = setting.AUE
APPID = setting.APPID
API_KEY = setting.TTS_API_KEY


def getHeader():
    curTime = str(int(time.time()))
    # ttp=ssml
    param = setting.HEAD_PARAM
    # print("param:{}".format(param))

    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    # print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))

    checkSum = m2.hexdigest()
    # print('checkSum:{}'.format(checkSum))

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    # print(header)
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()

def run_tts(words):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2), channels=1, rate=16000, output=True)

    r = requests.post(URL, headers=getHeader(), data=getBody(words))

    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
            # print(r.content)
            stream.write(r.content)  # 播放获得到的音频
            # writeFile("audio/" + sid + ".wav", r.content)
        else:
            # print(r.content)
            stream.write(r.content)  # 播放获得到的音频
            # writeFile("audio/" + "xiaoyan" + ".mp3", r.content)
        # print("success, sid = " + sid)
    else:
        print(r.text)

if __name__ == '__main__':
    words = "环境和健康息息相关保护环境促进健康"
    run_tts(words)