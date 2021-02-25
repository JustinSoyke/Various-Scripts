"""
Encryption Assignment -- Justin Soyke

Version: 0.1

Buttons:

Encrypt: This button encrypts the text which is in the text field and outputs the response

SQL Store: This button stores the encrypted message into the Database

SQL Retrieve: This button retrieves our encrypted message from the Database

Output: This is where the results are displayed

Other:
I have decided to use Fernet from the cryptography library as our encryption cipher
I have also decided to use MySQL as the Database Server. This Database Server is running on a Linux Virtual Machine

To-Do:
1. Change it so I DONT have to Hard Code the Secret Key for our Encryption
2. Add and use Self Signed Certificates
3. Clean up output a little
4. Add Exceptions


Bugs:


"""

# Imports

from PyQt5 import QtWidgets as widget
import sys
from cryptography.fernet import Fernet
import pymysql.cursors


class BaseWindow(widget.QMainWindow):
    """ The base window class"""
    def __init__(self):
        """ Initiates the Base Window UI"""

        super().__init__()
        self.startUI()

    def startUI(self):
        """ Starts the User Interface """

        # Encrypt Label
        encryptLabel = widget.QLabel(self)
        encryptLabel.setText("Encrypt: ")
        encryptLabel.move(10, 10)

        # Encryption Input Field
        self.encryptEdit = widget.QLineEdit(self)
        self.encryptEdit.move(75, 15)
        self.encryptEdit.resize(75, 20)
        self.encryptEdit.setFixedWidth(210)

        # Encryption Button
        encryptButton = widget.QPushButton("Encrypt", self)
        encryptButton.clicked.connect(self.encryptText)
        encryptButton.move(10, 40)
        encryptButton.resize(75, 20)

        # SQL Store Button
        sqlStoreButton = widget.QPushButton("SQL Store", self)
        sqlStoreButton.clicked.connect(self.sqlUpdate)
        sqlStoreButton.move(100, 40)
        sqlStoreButton.resize(75, 20)

        # SQL Retrieve Button
        sqlGetButton = widget.QPushButton("SQL Retrieve", self)
        sqlGetButton.clicked.connect(self.sqlRetrieve)
        sqlGetButton.move(200, 40)
        sqlGetButton.resize(75, 20)

        # Output Label #
        outputLabel = widget.QLabel(self)
        outputLabel.setText("Output: ")
        outputLabel.move(10, 100)

        # Output Form #
        self.outputForm = widget.QTextEdit(self)
        self.outputForm.move(10, 130)
        self.outputForm.setFixedHeight(200)
        self.outputForm.setFixedWidth(320)

        self.resize(450, 380)
        self.show()

    def encryptText(self):
        """ Function to encrypt our text in the input field"""
        #self.key = b'KtsHgRhukXABM_A-PiFvcUn0IJqARJpWys6wT4b68TE='
        self.file = open("encrypted-text.txt", "wb")
        self.f = Fernet(self.key)
        text = self.encryptEdit.text()
        text2 = bytes(text, 'utf-8')
        ciphertext = self.f.encrypt(text2)
        self.file.write(ciphertext)
        self.file.close()
        self.fileOpen = open("encrypted-text.txt", "rb")
        decrypt = self.f.decrypt(self.fileOpen.read())
        output = """
Input: %s
\nCiphertext: %s
\nDecrypted: %s
""" % (self.encryptEdit.text(), ciphertext, decrypt)

        self.outputForm.setText(output)
        return ciphertext  # Returns the Cipher Text so it can be used by other functions

    def sqlUpdate(self):
        """ Updates the encrypted message to the Database"""
        self.connection = pymysql.connect(host='192.168.220.135',
                                        user='user',
                                        password='password',
                                        db='messages',
                                        cursorclass=pymysql.cursors.DictCursor)

        try:
            with self.connection.cursor() as cursor:
                text = self.encryptText()
                text2 = text.decode('utf-8')
                print(text2)
                sql = ("UPDATE messages SET message = '%s' WHERE id = 1;" % (text2))
                print(sql)
                cursor.execute(sql)
                self.connection.commit()

        finally:
            self.connection.close()
            print(self.encryptText())

    def sqlRetrieve(self):
        """ Retrieves our Encrypted message from the Database and decrypts it"""
        try:
            self.connection = pymysql.connect(host='192.168.220.135',
                                              user='user',
                                              password='password',
                                              db='messages',
                                              cursorclass=pymysql.cursors.DictCursor)

            with self.connection.cursor() as cursor:
                f = Fernet(self.key)
                sql = ("SELECT * FROM messages WHERE id = 1;")
                print(sql)
                cursor.execute(sql)
                results = cursor.fetchone()
                print(results)
                decrypt = f.decrypt(results["message"])

                print(decrypt)
                output = "SQL Row: %s\n\nDecrypted Message: %s\n" % (results, decrypt)
                self.outputForm.clear()
                self.outputForm.setText(output)
        finally:
            self.connection.close()
            print("Finished")

    key = b'KtsHgRhukXABM_A-PiFvcUn0IJqARJpWys6wT4b68TE='  # Secret Key -- SHOULDN'T DO THIS!!!!

if __name__ == "__main__":  # Initiates Script
        app = widget.QApplication(sys.argv)
        baseWin = BaseWindow()
        app.exec_()
