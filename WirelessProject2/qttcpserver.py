#!/usr/local/bin/python3

from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
from PyQt5 import QtWidgets as widget
import sys
import time
from PyQt5 import QtNetwork as network
import re
import json

class BaseWindow(widget.QMainWindow):
    """ Main Window class"""
    def __init__(self):
        """ Initiates the Base Window UI"""

        super().__init__()
        self.startUI()

    def startUI(self):
        """ Starts the User Interface """


        self.welcomeMsg = widget.QLabel(self)
        self.welcomeMsg.setGeometry(core.QRect(10,10,200,25))
        self.welcomeMsg.setText("Welcome to Meadowbank Tafe, ")

        self.name = widget.QLabel(self)
        self.name.setGeometry(core.QRect(210, 10, 180, 25))
        self.name.setText("None")

        self.plateLabel = widget.QLabel(self)
        self.plateLabel.setGeometry(core.QRect(10, 70, 100, 25))
        self.plateLabel.setText("License Plate: ")

        self.plate = widget.QLabel(self)
        self.plate.setGeometry(core.QRect(100, 70, 140, 25))
        self.plate.setText("None")

        self.balanceLabel = widget.QLabel(self)
        self.balanceLabel.setGeometry(core.QRect(10, 45, 100, 25))
        self.balanceLabel.setText("Available Funds: ")

        self.balance = widget.QLabel(self)
        self.balance.setGeometry(core.QRect(120, 45, 60, 25))
        self.balance.setText("None")

        self.resize(600, 400)
        self.showMaximized()
        #time.sleep(3)
        self.startServer()

    def startServer(self):

        self.process = core.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)

        self.process.start("sudo", ["python3", "test.py"])

    def stdoutReady(self):
        text = self.process.readAll().data().decode()
#        self.name.clear()
  #      print(text,file=sys.stdout)

        if self.is_json(text):
            try:
                data = json.loads(str(text))
                print(data["name"],data["plate"],str(data["balance"]))
                self.name.setText(str(data["name"]))
                self.plate.setText(str(data["plate"]))
                self.balance.setText(str(data["balance"]))
            except KeyError:
                #pass
                print("Err")
            except ValueError:
                print("err2")
                #pass
        else:
            print(text)
#            self.name.setText(text)
#            pass


    def is_json(self, data):
        try:
            j_data = json.loads(data)
        except ValueError as e:
            return False
        return True

    def stderrReady(self):
        text = self.process.readAllStandardError().data().decode()
  #      self.test.clear()
        if self.is_json(text):
            data = json.loads(text)
            self.name.setText(data["name"])
            self.plate.setText(data["plate"])
            self.balance.setText(data["balance"])
        else:            #self.test.setText(text)
            print(text) 
 #           pass

        #data = json.loads(text)
        #print(dict(data))
        #self.test.setText(dict(data["Test"]))
        #print(text)

if __name__ == "__main__":
    try:
        app = widget.QApplication(sys.argv)
        baseWin = BaseWindow()
        app.exec_()
    finally:
        BaseWindow.process.kill
