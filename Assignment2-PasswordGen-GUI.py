# Password Generator
#  This Script Generates a 6 Character Password, using a conversion from ascii to Binary
#  which then counts the number of 1's and 0's, and uses the actual count to pick
#  a password Character from "abc", followed by a random number "0-9"
#  Week2 Programming Assignment ~ Written by Justin Soyke

import tkinter as tk
import re
import time
import datetime
import random


# ==GlobalConfig== #
passw = []
abc = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ" * 10
num = "0123456789"
debug = False  # Set to True to enable Debug Button which shows inputs in Console
# ================= #


def strip(self):
    strpName = re.sub(r'[^a-zA-Z\- ]', r'', self)
    return strpName  # Returns the output to be used in other functions

# Function Strips all except a-z, A-Z and '-', for names with a hyphen
# and returns the output so it can be used in other functions

def showOutput():
        output.configure(state='normal')
        output.delete(1.0, tk.END)
        output.insert(tk.END, "First Name: %s\nLast Name: %s\nDate of Birth: %s\n"
                              "Age: %s\nName Binary: %s\nGenerated Password: %s \n" % (strip(fname.get()),
                    strip(lname.get()), dobStr.get(), getAge(), nameBin(), passGen()))
        output.configure(state='disabled')
        passw = []

# Function to output results in in output field
# Makes the output writeable, It then Inputs the text

def getAge(): # Function to calculate Age from Date of Birth
    try:
        time.strptime(mdob.get(), "%d/%m/%Y")  # Validates the Input Date of Birth
        dobAge = dobStr.get()
        yrAge = dobAge[6:]                     #
        totalYr = int(datetime.date.today().year) - int(yrAge)
        if int(datetime.date.today().month) < int(str(dobAge[3:5])):
            age = int(totalYr) - 1
        else:
            age = totalYr
        return age
    except ValueError as e:
        print("Error: %s" % e)
        output.configure(state='normal')
        output.delete(1.0, tk.END)
        output.insert(tk.END, "Error: Invalid Date of Birth. Enter as DD/MM/YYYY (21/02/1990).")
        output.configure(state='disabled')


def nameBin():  # Function Converts Full Name to Binary
    fnameByte = strip(fnameStr.get())
    lnameByte = strip(lnameStr.get())
    fullnameByte = (fnameByte+lnameByte)
    fullnameBin = (' '.join(map(bin, bytearray(str(fullnameByte), 'ascii'))))
    return fullnameBin


def passGen():  # Function to Generate Password from 1's & 0's count
    passw = []  # Clears passw list each time function is used
    fnameGen = strip(fnameStr.get())
    lnameGen = strip(lnameStr.get())
    dobGen = dobStr.get()
    ageGen = getAge()
    for i in fnameGen, lnameGen, dobGen, ageGen:  # Goes through each Character and Converts to Binary
        bname = (','.join(map(bin, bytearray(str(i), 'ascii'))))
        one = 0
        zero = 0
        for x in bname:
            if "1" in x:
                one += 1
            elif "0" in x:
                zero += 1
        passw.append(abc[int(one)])  # Uses 1/0 Count to choose a Password Character
        passw.append(abc[int(zero)])
        print("Total Ones: %s Total Zeroes: %s" % (one, zero))
    passwd = ''.join(passw) # Joins all Characters to the one string
    passwdGen = (passwd[:5] + random.choice(num))
    return passwdGen


def showDebug():  # Function to print inputs to console
    print("Console Debug: \nFirst Name: %s\nLast Name: %s\nDate of Birth: %s\n"
          "Age:%s\nPassword: %s\nBinary Name: %s\n" % (
        fnameStr.get(), lnameStr.get(), dobStr.get(), getAge(), passw, nameBin()))


# =====Tkinter Config===== #
mgui = tk.Tk()
mgui.title("Password Generation")
dobStr = tk.StringVar()
fnameStr = tk.StringVar()
lnameStr = tk.StringVar()
fname = tk.Entry(mgui, textvariable=fnameStr)
lname = tk.Entry(mgui, textvariable=lnameStr)
mdob = tk.Entry(mgui, textvariable=dobStr)
output = tk.Text(mgui, height=10, width=38)

# =====Tkinter Labels====== #
tk.Label(mgui, text=" Please enter the following information:\n").grid(row=0)
tk.Label(mgui, text=" First Name (John): ").grid(row=2, column=0, sticky=tk.W, padx=5)
tk.Label(mgui, text=" Last Name (Doe):").grid(row=3, sticky=tk.W, padx=5)
tk.Label(mgui, text=" Date of Birth (10/02/1990):").grid(row=4, sticky=tk.W, padx=5)
tk.Label(mgui, text=" Output:").grid(row=7, sticky=tk.W, padx=5)
tk.Label(mgui, text="\n").grid(row=10, rowspan=3)

# ===Tkinter Grid Layout=== #
#  Configures where the widgets are layed out

fname.grid(row=2, column=1, sticky=tk.E, padx=10)
lname.grid(row=3, column=1, sticky=tk.E, padx=10)
mdob.grid(row=4, column=1, sticky=tk.E, padx=10)
output.grid(row=9, column=0, sticky=tk.E, columnspan=2, padx=10, ipadx=20)

# ===Tkinter Buttons=== #
tk.Button(mgui, text='Close', command=mgui.quit, width=10).grid(row=10, column=1, sticky=tk.E, padx=8)
tk.Button(mgui, text='Submit', command=showOutput, width=10).grid(row=10, column=0, sticky=tk.W, padx=8)
if debug:  # if debug = True, It enables the Debug Button
    tk.Button(mgui, text='Debug', command=showDebug, width=10).grid(row=10, column=2, sticky=tk.W)
else:
    pass
# ======================== #

if __name__ == "__main__":  # Runs the Tkinter App
    mgui.mainloop()
