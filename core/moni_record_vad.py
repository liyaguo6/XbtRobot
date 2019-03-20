# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 进行音频检测，当音量超过设定的阈值则开始录音，并将录音的结果存储到wav文件中
'''

import pyaudio
import wave
import numpy as np
import webrtcvad
import sys
from setting import settings
from core.MyRobert import MyThread
from core import wav2pcm
from core.utilties import random_start_terms
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1

CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge
NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2

vad = webrtcvad.Vad(1)

class Monitor():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        # self.Voice = False
        self.NoVoiceFlag =False


    def start(self):
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        self.frames = []

    def run(self,isinterrupt=False):
        count = 0
        while True:
            count += 1
            print("开始第" + str(count) + "次检测")  # 设置循环20次时，停止运行程序
            res = self.monitor()

            if res :
                self.record()
                self.stop()
                self.write_audio_to_wave(settings.LISTEN_FILE)
                # self.VoiceFlag= False
                count = 0
                break
            # elif self.flag:
            #     break
            elif count == 10:  # 设置循环20次时，返回flag=True的信息
                self.NoVoiceFlag = True
                count =0
                break
            if isinterrupt ==False:
                if count == 3:
                    # t2 = MyThread(wav2pcm.audio_play, args=(self.start_term_path,))
                    # t2.start()
                    wav2pcm.audio_play(self.start_term_path)

    def monitor(self):

        # while True:
            self.start()
        #     self.count += 1
        #     print("开始第" + str(self.count) + "次检测")  # 设置循环20次时，停止运行程序

            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                self.frames.append(data)
            audio_data = np.fromstring(data, dtype=np.short)
            # large_sample_count = np.sum( audio_data > 800 )
            temp = np.max(audio_data)   # 使用最大因音量来控制
            if temp > 800:
                return True
            else:
                self.frames = []

    @property
    def start_term_path(self):
        return random_start_terms()

    def record(self):
        # res = self.monitor()
        # if res:
        # if res and not self.flag:
            print("检测到信号，开始录音")
            ring_buffer_flags_end = [1] * NUM_WINDOW_CHUNKS_END
            ring_buffer_index_end = 0

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS * 30)):
                data = self.stream.read(CHUNK_SIZE)
                self.frames.append(data)
                active = vad.is_speech(data, RATE)

                # sys.stdout.write('1' if active else '_')

                ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                ring_buffer_index_end += 1
                ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

                num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                if num_unvoiced > 0.96 * NUM_WINDOW_CHUNKS_END:                     # num_unvoice超过一定阈值，停止录音
                    break
            print("录音结束")
            # self.stop()


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        # self.p.terminate()     #注释掉，使循环继续

    # def __del__(self):
    #     self.p.terminate()

    def write_audio_to_wave(self, file_name):
        """ Write saved audio byte data to a file

        recordLen: length in seconds to record
        outWaveFile: filename to write wave file to

        """
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.p.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()


if __name__ == '__main__':
    monitor = Monitor()
    for i in range(3):
        monitor.run()




