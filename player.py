import cv2
import numpy as np
import time
from ffpyplayer.player import MediaPlayer
from datetime import timedelta
from statusBar import *


class Player:
    def __init__(self, file, algorithm, args):
        self.__file = args[0]
        self.__deficiency = args[1]
        self.__threads = args[2]
        self.__fpsLock = args[3]

        self.__algorithm = algorithm

        self.__cap = cv2.VideoCapture(self.__file)
        self.__width = int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__fps = self.__cap.get(cv2.CAP_PROP_FPS)
        self.__frames = self.__cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__curpos = self.__cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        self.__length = int(self.__frames / self.__fps)
        self.__curposF = "{:8>}".format(str(timedelta(seconds=int(self.__curpos))))
        self.__lengthF = "{:8>}".format(str(timedelta(seconds=self.__length)))

        self.__sb = StatusBar(64, self.__width-64, self.__height-14)
        self.__currentFrame = 0

        self.__pause = False
        cv2.namedWindow("Test")
        cv2.moveWindow("Test", 0, 0)
        cv2.setMouseCallback("Test", self.mouse)

        self.__timestart = 0
        self.__pausetime = 0
        self.__pausetimer = 0

        self.__player = 0

    def mouse(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN and self.__sb.show==False:
            self.__pause = not self.__pause
            if self.__pause == False:
                # if self.__pausetimer != 0:
                #     self.__pausetime = time.perf_counter() - self.__pausetimer
                #     self.__timestart = self.__timestart - self.__pausetime
                #     self.__pausetimer = 0

                self.__player.seek(self.__currentFrame / self.__fps, relative=False, accurate=False)

        if event == cv2.EVENT_MOUSEMOVE and self.__pause==True:
            self.__sb.delayF = int(self.__sb.delayS * self.__fps)
            pos = int(self.__currentFrame * self.__sb.len/self.__frames)

            if x in range(self.__sb.start+pos-10, self.__sb.start+pos+10) and y in range(self.__sb.top - 5, self.__sb.top + 5):
                self.__sb.show = True
            else:
                self.__sb.show = False
            if flags == 1:
                self.__sb.show = True

                xx = 1 if x-self.__sb.start<10 else x-self.__sb.start
                if x - self.__sb.start > self.__sb.len:
                    xx = self.__sb.len
                self.__currentFrame = int(xx/(self.__sb.len/self.__frames))-1

    def showPause(self, img,x,y):
        s_img = cv2.imread("img/play.png", -1)
        x1, x2 = x - int(s_img.shape[0] / 2), x + int(s_img.shape[0] / 2)
        y1, y2 = y - int(s_img.shape[1] / 2), y + int(s_img.shape[1] / 2)
        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            img[x1:x2, y1:y2, c] = (alpha_s * s_img[:, :, c] + alpha_l * img[x1:x2, y1:y2, c])
        return img

    def pb(self, img, frame):
        pos = int(frame * self.__width/self.__frames)
        img = cv2.line(img, (0,self.__height), (pos,self.__height), (255, 255, 0), 6)
        return img

    def pbS(self, img, frame):
        pos = int(frame * self.__width / self.__frames)
        img = cv2.line(img, (0, self.__height), (pos, self.__height), (255, 128, 0), 10)
        return img

    def sb(self, img, frame):
        tmp = img[(self.__sb.top - 40):self.__height,0:self.__width]
        self.tm = tmp.copy()
        pos = int(frame * self.__sb.len/self.__frames)
        mtime = "{:8>}".format(str(timedelta(seconds=int(frame/self.__fps))))

        img = cv2.putText(img, mtime, (5,self.__sb.top+4),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        img = cv2.putText((img), self.__lengthF, (self.__sb.final + 10, self.__sb.top + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                          (255, 255, 0), 1)
        img = cv2.circle((img), (self.__sb.start + pos, self.__sb.top), 5, (255, 255, 0), 4)
        img = cv2.line((img), (self.__sb.start, self.__sb.top), (self.__sb.final, self.__sb.top), (255, 255, 0), 1)

        return img


    def run(self):
        self.__timestart = time.perf_counter()

        cap = cv2.VideoCapture(self.__file)
        ret, img = cap.read()
        x, y, z = img.shape

        tr = 32

        self.__player = MediaPlayer(self.__file)

        if self.__deficiency == "P":
            while cap.isOpened():
                if not self.__pause:
                    ret, img = cap.read()
                    self.__currentFrame+=1
                    if ret == True:
                        self.__player.set_pause(False)

                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        img = self.__algorithm.threadPro(img, x, y, z, int(self.__threads))

                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                        img = self.sb(img, self.__currentFrame)

                        if self.__fpsLock=="True":
                            while time.perf_counter()-self.__timestart < self.__currentFrame / self.__fps:
                                pass

                        cv2.imshow("Test", img)
                    else:
                        break
                else:
                    # self.__pausetimer =  time.perf_counter()
                    self.__player.set_pause(True)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, self.__currentFrame)
                    ret, img = cap.read()
                    img = self.sb(img, self.__currentFrame)
                    self.showPause(img, int(x / 2), int(y / 2))

                    cv2.imshow("Test", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        elif self.__deficiency == "D":
            while cap.isOpened():
                if not self.__pause:
                    ret, img = cap.read()
                    self.__currentFrame += 1
                    if ret == True:
                        self.__player.set_pause(False)

                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        img = self.__algorithm.threadDeu(img, x, y, z, tr)

                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                        img = self.sb(img, self.__currentFrame)

                        if self.__fpsLock == "True":
                            while time.perf_counter() - self.__timestart < self.__currentFrame / self.__fps:
                                pass

                        cv2.imshow("Test", img)
                    else:
                        break
                else:
                    self.__pausetimer = time.perf_counter()
                    self.__player.set_pause(True)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, self.__currentFrame)
                    ret, img = cap.read()
                    img = self.sb(img, self.__currentFrame)
                    self.showPause(img, int(x / 2), int(y / 2))

                    cv2.imshow("Test", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        elif self.__deficiency  == "T":
            while cap.isOpened():
                if not self.__pause:
                    ret, img = cap.read()
                    self.__currentFrame += 1
                    if ret == True:
                        self.__player.set_pause(False)

                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        img = self.__algorithm.threadTri(img, x, y, z, tr)

                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                        img = self.sb(img, self.__currentFrame)

                        if self.__fpsLock == "True":
                            while time.perf_counter() - self.__timestart < self.__currentFrame / self.__fps:
                                pass

                        cv2.imshow("Test", img)
                    else:
                        break
                else:
                    self.__pausetimer = time.perf_counter()
                    self.__player.set_pause(True)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, self.__currentFrame)
                    ret, img = cap.read()
                    img = self.sb(img, self.__currentFrame)
                    self.showPause(img, int(x / 2), int(y / 2))

                    cv2.imshow("Test", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        durata = time.perf_counter() - self.__timestart
        print(durata)

        # print("Threads",tr)
        # print(int(y / int(tr / 2)))
        # print(int(x / 2))

        cap.release()
        cv2.destroyAllWindows()
