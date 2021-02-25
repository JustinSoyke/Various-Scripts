"""
Major Project Script - SQLite3
Version: 0.3

About:
Retrieve User Records and Displays Entry, allows us to update entry
Secured with a Login page which checks credentials against the Database

What's New:

1. Added Login Page that checks against a database :D


Buttons:

Search: This Button searches the Database with the Surname, and displays results
in the Output Section.

Open Details:
Opens the SQL Entry and displays the Data Retrieved

PopupWindow:

This window displays the data from the SQL Database.
It allows us to edit the fields, and upload a new Image to the Database


To-Do:
1. Add error checking -- Complete
2. Fix bugs
3. Clean up code
4. User a more secure Password Hash (Currently using MD5)


Bugs:
1. There is no error checking currently, program crashes a lot  -- Fixed!
2. Image doesn't scale down small enough, due to the high resolution of the picture from mobile
3. Crashes, crashes and more crashes, especially on errors
4. You "Have" to select an image to update the entry, otherwise it crashes *I will fix this!* -- Fixed!

"""

# Imports

from PyQt5 import QtWidgets as widget
from PyQt5.QtGui import QPixmap as qp
from PyQt5 import QtCore as core
import sys
import sqlite3
import re
import hashlib

class Login(widget.QDialog):
    """ Login Window Class"""
    def __init__(self, parent=None):
        """ Init and set User Interface"""
        super(Login, self).__init__(parent)

        # User Label #
        self.userLabel = widget.QLabel(self)
        self.userLabel.setText("User: ")
        self.userLabel.move(10,10)

        # Username Entry Form #
        self.userForm = widget.QLineEdit(self)
        self.userForm.move(80,10)
        self.userForm.resize(75, 18)

        # Password Label #
        self.passLabel = widget.QLabel(self)
        self.passLabel.setText("Password: ")
        self.passLabel.move(10, 40)

        # Password Form #
        self.passForm = widget.QLineEdit(self)
        self.passForm.move(80, 40)
        self.passForm.resize(75, 18)
        self.passForm.setEchoMode(widget.QLineEdit.Password)

        # Login Button #
        self.loginButton = widget.QPushButton(self)
        self.loginButton.setText("Login")
        self.loginButton.clicked.connect(self.checkUser)
        self.loginButton.move(20,90)

        # Misc Settings #
        self.setWindowTitle("Login")
        self.resize(200,200)


    def checkUser(self):
        """Checks Login Credentials against Database"""
        conn = sqlite3.connect("health_records.db")
        loginSql = "SELECT username, password from h_users WHERE userid=1;"
        cursor = conn.execute(loginSql)  # Execute loginSql SQL
        results = cursor.fetchone()  # Retrieve the Results from SQL Statement
        password = self.passForm.text()
        hashpw = hashlib.md5(password.encode("utf-8")).hexdigest()  # Get the MD5 Hash of Password entered
        if self.userForm.text() == results[0] and hashpw == results[1]:
            # If Details entered are correct, login :)
            print("Success")
            self.accept()
        else:
            widget.QMessageBox.warning(self, "Error", "Incorrect Username or Password Combination")



class BaseWindow(widget.QMainWindow):
    """ The base window class"""
    def __init__(self):
        """ Initiates the Base Window UI"""

        super().__init__()
        self.startUI()

    def startUI(self):
        """ Starts the User Interface """

        self.searchLabel = widget.QLabel(self)
        self.searchLabel.setText("Lookup Surname: ")
        self.searchLabel.move(10, 5)

        self.searchEdit = widget.QLineEdit(self)
        self.searchEdit.move(100, 10)
        self.searchEdit.resize(75, 18)
        self.searchEdit.setFixedWidth(75)

        searchButton = widget.QPushButton("Search", self)
        searchButton.clicked.connect(self.search)
        searchButton.move(200, 10)
        searchButton.resize(75, 20)

        # Details Button
        detailsButton = widget.QPushButton("Open Details", self)
        detailsButton.clicked.connect(self.outputWindow)
        detailsButton.move(200, 40)
        detailsButton.resize(75, 20)

        # Output Label #
        outputLabel = widget.QLabel(self)
        outputLabel.setText("Output: ")
        outputLabel.move(10, 100)

        # Output Form #
        self.outputForm = widget.QTextEdit(self)
        self.outputForm.move(10, 130)
        self.outputForm.setFixedHeight(200)
        self.outputForm.setFixedWidth(320)

        # Window Title #
        self.setWindowTitle("Database Records Lookup - Justin Soyke")

        self.resize(450, 380)

    def strip(self, s):
        """
        Strips invalid Input to prevent SQL Injections

        Takes a user input and strips all invalid characters to prevent an SQL injection vulnerability

        Parameters:
            s: This is the user input

        Returns:
            strpName: Returned Stripped User Input to be used in other functions

        """


        strpName = re.sub(r'[^a-zA-Z\- ]', r'', s)
        return strpName  # Returns the output to be used in other functions

    def search(self):
        """Search the Database and display entry in Output window"""
        conn = sqlite3.connect("health_records.db")
        cursor = conn.cursor()
        searchfield = self.searchEdit.text()
        print(searchfield)
        sql = "SELECT id, fname, lname, dob, address FROM h_records WHERE lname LIKE '%s'" % self.strip(str(searchfield))
        cursor.execute(sql)
        results = cursor.fetchone()
        self.outputForm.setText(str(results))

    def retrieve(self):
        """Retrieves the Row to be used in Details Window"""
        conn = sqlite3.connect("health_records.db")   # Define Database
        cursor = conn.cursor()
        sql = "SELECT * FROM h_records WHERE id=2;"
        cursor.execute(sql)
        self.results = cursor.fetchone()
        return self.results

    def outputWindow(self):
        """Opens the Details in a Popup Window"""
        self.resultView = PopupWindow(self)
        self.resultView.show()

class PopupWindow(widget.QDialog):
    """Popup Window Class"""
    def __init__(self, parent):
        super().__init__(parent)
        res = BaseWindow.retrieve(self)
        self.id = res[0]
        self.fname = res[1]
        self.lname = res[2]
        self.dob = res[3]
        self.address = res[4]
        self.image = res[5]

        self.setWindowTitle("Details for %s, %s" % (self.lname, self.fname))

        # Image - Pixmap  #
        self.pixmap = qp()
        self.pixmap.loadFromData(self.image)  # Loads Binary Data to be used
        self.pix = widget.QLabel(self)
        self.pix.setPixmap(self.pixmap)
        self.pix.move(256, 25)
        self.pix.setMaximumWidth(128)
        self.pix.setMaximumHeight(128)
        self.pixmap.scaled(128, 128, core.Qt.IgnoreAspectRatio, core.Qt.SmoothTransformation)

        # ID Section #
        self.labelID = widget.QLabel(self)
        self.labelID.setText("ID: ")
        self.labelID.move(10,30)

        self.fieldID = widget.QLineEdit(self)
        self.fieldID.move(100, 30)
        self.fieldID.resize(140, 15)
        self.fieldID.setText(str(self.id))
        self.fieldID.setDisabled(True)

        # First Name Section #
        self.fnameLabel = widget.QLabel(self)
        self.fnameLabel.setText("First Name: ")
        self.fnameLabel.move(10, 50)

        self.fnameField = widget.QLineEdit(self)
        self.fnameField.move(100, 50)
        self.fnameField.resize(140, 15)
        self.fnameField.setText(str(self.fname))

        # Last Name Section #
        self.lnameLabel = widget.QLabel(self)
        self.lnameLabel.setText("Last Name: ")
        self.lnameLabel.move(10, 70)

        self.lnameField = widget.QLineEdit(self)
        self.lnameField.move(100, 70)
        self.lnameField.resize(140, 15)
        self.lnameField.setText(str(self.lname))

        # Date of Birth Section #
        self.dobLabel = widget.QLabel(self)
        self.dobLabel.setText("Date of Birth: ")
        self.dobLabel.move(10, 90)

        self.dobField = widget.QLineEdit(self)
        self.dobField.move(100, 90)
        self.dobField.resize(140, 15)
        self.dobField.setText(str(self.dob))

        # Address Section #
        self.addressLabel = widget.QLabel(self)
        self.addressLabel.setText("Address: ")
        self.addressLabel.move(10, 110)

        self.addressField = widget.QLineEdit(self)
        self.addressField.move(100, 110)
        self.addressField.resize(140, 15)
        self.addressField.setText(str(self.address))

        # Image Section #
        self.imageLabel = widget.QLabel(self)
        self.imageLabel.move(290,5)
        self.imageLabel.setText("Patient Image")

        self.browseImage = widget.QPushButton("Browse", self)
        self.browseImage.clicked.connect(self.fileDialog)
        self.browseImage.move(290, 160)

        # Update SQL Entry Section #
        self.updateButton = widget.QPushButton("Update", self)
        self.updateButton.clicked.connect(self.updateEntry)
        self.updateButton.move(10, 150)

        self.show()  # Show the User Interface

        self.resize(450, 380)  # Resize the Window

    def strip(self, s):
        """Strip Invalid Characters from our Input"""
        strpName = re.sub(r'[^a-zA-Z0-9\-/ ]', r'', s)
        return strpName  # Returns the output to be used in other functions


    def updateEntry(self):
        """Function which Updates the Entry"""
        conn = sqlite3.connect("health_records.db")  # Connect to SQLite3 Database
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE h_records SET fname=(?), lname=(?), dob=(?), address=(?), image=(?) WHERE id=2;",
                       (self.strip(str(self.fnameField.text())), self.strip(str(self.lnameField.text())),
                    self.strip(str(self.dobField.text())),self.strip(str(self.addressField.text())), self.readFile,))
        except AttributeError:
            print("Didn't select an image, trying with no image ")
            cursor.execute("UPDATE h_records SET fname=(?), lname=(?), dob=(?), address=(?) WHERE id=2;",
                           (self.strip(str(self.fnameField.text())), self.strip(str(self.lnameField.text())),
                            self.strip(str(self.dobField.text())), self.strip(str(self.addressField.text())),))
        finally:
            conn.commit()
            self.results = cursor.fetchone()

    def fileDialog(self):
        """Browse for File Dialog"""
        try:
            self.openFile = widget.QFileDialog(self).getOpenFileName(self, 'Open File',
                            core.QDir.currentPath(), "Image Files *.jpg *.png")  # Browse Button for File
            if self.openFile:
                print(self.openFile[0])
                self.readFile = open(self.openFile[0], 'rb').read()
                print(self.readFile)
        except FileNotFoundError:
            print("File Not Found\nPlease try again")
            pass


if __name__ == "__main__":  # Initiates Script
        app = widget.QApplication(sys.argv)
        login = Login()
        login.show()  # Show the Login Form first
        if login.exec_() == widget.QDialog.Accepted:  # If Login is accepted: show main window
            baseWin = BaseWindow()
            baseWin.show()   # Show the Main Window IF login is successful
            app.exec_()

