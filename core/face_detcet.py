import cv2
import os
import time
import threading
# 实例化人脸分类器
# face_cascade = cv2.CascadeClassifier('../database/haarcascades/haarcascade_frontalface_default.xml')
import numpy as np


# cap = cv2.VideoCapture(0)
# while True:
#     # 抓取一帧视频q
#     ret, frame = cap.read()
#     # Our operations on the frame come here
#
#     # Display the resulting frame
#     # 将原彩色图转换成灰度图
#     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.2, 8)
#     for (x, y, w, h) in faces:
#     #     # 在原彩色图上画人脸矩形框
#         img=cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         cv2.imshow('frame', img)
#         # print(x, y, w, h)
#     # 遍历人脸检测结果(x,y)左上角坐标，(x+w,y+h)右下角坐标
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

class FaceRecon():
    def __init__(self,path):
        self.face_cascade= cv2.CascadeClassifier(path)
        self.video = cv2.VideoCapture(0)
        self.frame =None
        self.is_face = False
        self.quit = False
    def capture_image(self):
        # 抓取一帧视频q
        ret, self.frame = self.video.read()
        # 在这个视频中循环遍历每个人人脸
        self.gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)


    def detection(self):


        self.faces = self.face_cascade.detectMultiScale(self.gray, 1.2, 8)
        if isinstance(self.faces,np.ndarray):
            self.is_face = True
            for (x, y, w, h) in self.faces:
                cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0, 0, 255),4)
        else:
            self.is_face = False

    def close(self):
            self.quit = True
            self.video.release()
            cv2.destroyAllWindows()

    def imag_show(self):
        while not self.quit:
            self.capture_image()
            self.detection()
            cv2.imshow('Video', self.frame)
            # print(self.is_face)
            cv2.waitKey(1)



if __name__ == '__main__':
    fr = FaceRecon('../database/haarcascades/haarcascade_frontalface_default.xml')
    t = threading.Thread(target=fr.imag_show)
    t.start()

    # while 1:
    #     time.sleep(3)