import difflib
import os
import random
import sys
import threading
import time
import speech_recognition as sr
from PyQt5 import QtWidgets, QtCore
from qtpy import QtGui

from myInterface import Ui_MainWindow

r = sr.Recognizer()


def similarityBetween(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.helpFlag = False
        self.state = 0
        # 0 - sleeping
        # 1 - waked but no command
        # 2 - wake up fail
        # 3 - get command

    def wakeUp(self):
        print("Waiting for waking up...")
        self.state = 0
        self.ui.labelSorry.setVisible(False)
        self.ui.labelH2.setVisible(False)
        self.ui.labelH1.setVisible(False)
        self.ui.label2click.setVisible(True)
        microphone = sr.Microphone()
        with microphone as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print()

        try:
            myCommand = r.recognize_sphinx(audio)
        except():
            self.RecogFailed()
        else:
            print('Command: ' + myCommand)
            global similarity
            similarity = similarityBetween(myCommand, "hello")
            print("Similarity: ", similarity)

            if similarity > 0.1:
                self.WakedUpSuccess()
            else:
                self.WakeUpFailed()

    def RecogFailed(self):
        # Recognize failed
        print('Fail to recognize the audio.')
        global timer
        if self.state == 0:
            timer = threading.Timer(0.1, self.wakeUp)
            timer.start()
        elif self.state == 1:
            self.WakedUpSuccess()

    def WakedUpSuccess(self):
        # the voice assistant is waked up
        print('Waked up')
        global timer
        timer.cancel()
        self.state = 1
        self.helpFlag = False

        # set labels invisible
        self.ui.labelHello.setVisible(False)
        self.ui.label2click.setVisible(False)
        self.ui.labelHH.setVisible(False)
        self.ui.labelH1.setVisible(False)
        self.ui.labelH2.setVisible(False)
        self.ui.labelH3.setVisible(False)
        self.ui.labelH4.setVisible(False)

        # start the movement of gif
        # the closer to destination the lower the speed
        step = 0.5
        y = 50
        while y < 200:
            self.ui.voiceFig.setVisible(False)
            y += step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)
        step = 0.3
        while y < 250:
            self.ui.voiceFig.setVisible(False)
            y += step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)
        step = 0.2
        while y < 280:
            self.ui.voiceFig.setVisible(False)
            y += step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)
        step = 0.1
        while y < 300:
            self.ui.voiceFig.setVisible(False)
            y += step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)

        # add an over-moved animation effect
        step = 0.05
        while y < 310:
            self.ui.voiceFig.setVisible(False)
            y += step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)
        step = 0.02
        while y > 300:
            self.ui.voiceFig.setVisible(False)
            y -= step
            self.ui.voiceFig.move(85, int(y))
            self.ui.voiceFig.setVisible(True)
            time.sleep(0.0005)
        self.ui.labelWaked.setVisible(True)
        # 0.2s after movement, set the voiceFig to 'normal.gif'
        time.sleep(0.2)
        self.ui.voiceFig.setMovie(self.ui.gifNorm)

        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            command = r.recognize_sphinx(audio)
        except:
            self.RecogFailed()
        else:
            print('The statement you said is {' + command + '}')
            list = [similarityBetween(command, "music"),
                    similarityBetween(command, "note"),
                    similarityBetween(command, "google"),
                    similarityBetween(command, "calculate")]
            maxSim = max(list)
            maxIndex = list.index(maxSim)
            if maxSim < 0.2:
                self.ui.labelHello.setText("I guess you want to..")
                maxIndex = random.randint(0, 2)
            self.state = 3
            print("Similarity:" + str(list[maxIndex]))
            self.ui.labelWaked.setVisible(False)
            self.ui.labelRec.setVisible(True)
            self.ui.voiceFig.setVisible(False)
            self.ui.voiceFig.setMovie(self.ui.gifRecing)

            self.ui.voiceFig.setVisible(True)
            time.sleep(2)
            if maxIndex == 0:
                print("Playing Lemon.mp3")
                os.system("open resources/Lemon.mp3")
            elif maxIndex == 1:
                print("open Notability.app")
                os.system("open /Applications/Notability.app")
            elif maxIndex == 2:
                print("open Google.com")
                os.system("open https://google.com")
            else:
                print("open Calculator.app")
                os.system("open /System/Applications/Calculator.app")
            time.sleep(2)
            self.ui.labelWaked.setVisible(False)
            self.ui.labelHello.setVisible(True)
            self.ui.voiceFig.setVisible(False)
            self.ui.voiceFig.setGeometry(QtCore.QRect(85, 50, 150, 100))
            self.ui.voiceFig.setMovie(self.ui.gif)
            self.ui.voiceFig.setVisible(True)
            self.ui.labelRec.setVisible(False)
            timer = threading.Timer(0.1, self.wakeUp)
            timer.start()

    def WakeUpFailed(self):
        # the voice assistant is failed to be waked up
        self.state = 2
        print('Failed wake up')
        self.ui.labelSorry.setVisible(True)
        # invoke wakeUp() again
        time.sleep(0.5)
        self.wakeUp()

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        print('click click')
        global timer
        timer.cancel()
        if self.state != 0:
            return
        if self.helpFlag is True:
            self.helpFlag = False;
            self.ui.labelHello.setVisible(True)
            self.ui.label2click.setText("Double click to show help list.")
            self.ui.label2click.setVisible(True)
            timer = threading.Timer(0.1, self.wakeUp)
            timer.start()
        else:
            self.helpFlag = True
            self.ui.label2click.setText("Double click to return.")
            self.ui.labelHello.setVisible(False)
        self.ui.labelHH.setVisible(self.helpFlag)
        self.ui.labelH1.setVisible(self.helpFlag)
        self.ui.labelH2.setVisible(self.helpFlag)
        self.ui.labelH3.setVisible(self.helpFlag)
        self.ui.labelH4.setVisible(self.helpFlag)


if __name__ == '__main__':
    # get start
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    timer = threading.Timer(0.1, application.wakeUp)
    timer.start()
    sys.exit(app.exec())
