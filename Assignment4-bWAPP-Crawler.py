"""
bWAPP Website Crawler -- Assignment #4 Written by Justin Soyke

Version 0.01

~ PyQt5 Window

Functions(Buttons):

Crawls a bWAPP installation to all GET URLs

Test Login : Checks the credentials are correct
(default user:pass : test:test)

Crawl: Logs in with credentials, and crawls for URLs, displays results in Output

Preview HTML: Opens the Downloaded .html page in a popup window for preview

Other:
I have decided to use Python-Requests instead of Urllib as I have used urllib2
many times in the past, however I have found Python-Requests much easier, and (Faster?)
to use!
I have also used the BeautifulSoup library to help analyze the HTML code much more easily

To-Do:

1. Enumerate Found URLs and test against known vulnerabilities
2. Actually Crawl the URL in the URL Input lol
3. Add in features so we can crawl any website, not just the hardcoded bWAPP installation
4. Add in better error checking
5. Add urls clickable, so we can preview each link found


Known Bugs and problems:

Program hangs for a bit if you press Fuzz multiple times
Crashes, Crashes and more Crashes
PyQt5 still crashes upon errors, even with the error checking!!

"""

# Imports

import sys
from PyQt5 import QtWidgets as widget
from PyQt5 import QtWebEngineWidgets as web
from PyQt5 import QtCore as core
import requests
from bs4 import BeautifulSoup as bs
import time


class BaseWindow(widget.QMainWindow):
    """
    Base Window Class

    Functions:
    __init__: starts the startUI method
    startUI:  Loads up all the Fields, Labels and Buttons
    testLogin: Tests User Credentials
    findUrl:  Crawls Website for GET Urls
    showHtml: Previews Downloaded HTML in a Popup Window

    """

    def __init__(self):
        """ Initiates the Base Window UI"""

        super().__init__()
        self.startUI()

    def startUI(self):
        """ Sets all the Labels, Buttons, Input Fields"""

        self.setWindowTitle("Assignment #4 - Justin Soyke - Web Crawl")  # Set Window Title

        #  User Label #
        userLabel = widget.QLabel(self)  # Defines User Label
        userLabel.setText("User Name: ")
        userLabel.move(10, 10)  # Positions User Label

        # User Name Input #
        self.userEdit = widget.QLineEdit(self)
        self.userEdit.move(75, 15)
        self.userEdit.resize(75, 20)

        # Pass Label #
        passLabel = widget.QLabel(self)
        passLabel.setText("Password: ")
        passLabel.move(200, 10)

        # Password Input #
        self.passEdit = widget.QLineEdit(self)
        self.passEdit.move(260, 15)
        self.passEdit.resize(75, 20)
        self.passEdit.setEchoMode(widget.QLineEdit.Password)

        # Test Login Button #
        testButton = widget.QPushButton("Test Login", self)
        testButton.clicked.connect(self.testLogin)
        testButton.move(350, 15)
        testButton.resize(75, 20)

        # Url Label #
        urlLabel = widget.QLabel(self)
        urlLabel.setText("Url: ")
        urlLabel.move(10, 50)

        # Url Input #
        self.urlForm = widget.QLineEdit(self)
        self.urlForm.move(50, 55)
        self.urlForm.resize(75, 20)
        self.urlForm.setFixedWidth(210)

        # Fuzz Button #
        urlButton = widget.QPushButton("Crawl", self)
        urlButton.clicked.connect(self.findUrl)
        urlButton.move(350, 50)
        urlButton.resize(75, 20)

        # Output Label #
        outputLabel = widget.QLabel(self)
        outputLabel.setText("Output: ")
        outputLabel.move(10, 100)

        # Output Form #
        self.outputForm = widget.QTextEdit(self)
        self.outputForm.move(10, 130)
        self.outputForm.setFixedHeight(200)
        self.outputForm.setFixedWidth(320)

        # Crawl Result Label
        self.resultLabel = widget.QLabel(self)
        self.resultLabel.move(10, 340)
        self.resultLabel.setFixedWidth(200)

        # Preview HTML Button #
        htmlButton = widget.QPushButton("Preview HTML", self)
        htmlButton.clicked.connect(self.showHtml)
        htmlButton.move(350, 70)
        htmlButton.resize(75, 20)

        self.resize(450, 380)  # Resize Windows to x, y dimentions
        self.show()  # Shows Inputs, Labels, Buttons in the Main Window

    def testLogin(self):
        """ Test Login Credentials against Website"""
        try:
            self.details = {"login": "%s" % self.userEdit.text(), "password": "%s" % self.passEdit.text(),
                       "security_level": 0, "form": "submit"}

            print(self.details)

            with requests.session() as session:  # Create Login Session
                loginReq = session.post(loginURL, data=self.details)
                print(loginReq.url)
                if "portal" in loginReq.url:  # If redirects to portal.php = successful login
                    print("Login was Successful")
                elif "login" in loginReq.url:
                    print("Login Failed")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)
            return


    def findUrl(self):
        """Logs in using credentials, Crawls for all Urls"""
        try:
            urls.clear()
            self.details = {"login": "%s" % self.userEdit.text(), "password": "%s" % self.passEdit.text(),
                   "security_level": 0, "form": "submit"}
            with requests.session() as session:  # Create Session
                loginReq = session.post(loginURL, data=self.details)  # Login to website
                soup = bs(loginReq.text, "html.parser")  # Feed HTML to be analysed by BeautifulSoup
                htmlOutput.write(loginReq.text)  # Save HTML to html-preview.html
                findOpt = soup.find_all("option")
                # Use BeautifulSoup searching for all <Option> Tags -- Workaround to get all URLs on bWAPP
                for x in findOpt:  # for x in findOpt: x.get("value"), e.g 87
                    bugID = x.get("value")
                    if bugID not in pageID:  # If we don't already have that Bug ID append to pageID
                        pageID.append(bugID)
                    else:
                        continue

                tstart = time.clock()  # Start Timer!

                # We have to submit a form, to retrieve the URL, #TooManyRequests
                for i in pageID:
                    getUrlData = {"bug":"%d" % int(i), "form":"submit"}
                    getUrlReq = session.post(url, data=getUrlData)
                    urls.append(i)  # Append URL Found to urls list
                    self.outputForm.append(getUrlReq.url)  # Add the URL to Output Form
                    self.outputForm.setReadOnly(True)  # Change to ReadOnly to prevent loss of data
                    #time.sleep(0.05) # Give me some sleep! :D

                tend = time.clock() - tstart  # Total Time It took!
                self.resultLabel.setText("Found %s URLs in %s Seconds" % (len(urls), int(tend)))
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def showHtml(self):
        """Load HTML Output In PopupWindow"""
        self.htmlView = PopupWindow(self)
        self.htmlView.show()  # Open Popup Window


class PopupWindow(widget.QDialog):
    """ Popup Window Class for QDialog"""
    def __init__(self, parent):
        """ Defines everything in the Popup Window, opens Saved .html"""
        super().__init__(parent)
        self.webView = web.QWebEngineView(self)
        self.webView.load(core.QUrl("file:///FILE_HERE"))
        self.webView.resize(600, 400)
        self.setWindowTitle("Website Preview -- %s" % url)  # Set Dialog Window Title

# Global Configuration #

url = "http://192.168.43.186/bWAPP/portal.php" #http://192.168.1.8/bWAPP/portal.php"
loginURL = "http://192.168.43.186/bWAPP/login.php"
pageID = []  # Bug ID List
urls = []  # Crawled Url List
htmlOutput = open("website-preview.html", "w")
htmlInput = open("website-preview.html", "r")
########################

if __name__ == "__main__":  # Initiates Script
        app = widget.QApplication(sys.argv)
        baseWin = BaseWindow()
        app.exec_()
