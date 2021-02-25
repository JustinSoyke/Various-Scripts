"""
SQL Search Tkinter - Written by Justin Soyke - Assignment #3 2018

Version 0.01

Functions:
Enables a search of an SQLITE3 Database using GUI with TKinter
Outputs the SQL Result in a Grid, button enables to retrieve the SQL Row
Strips illegal characters from Input (i.e ' " ` )

Known Bugs:

1. SQL Result Grid does not clear the previous result.
2.

What needs to be done?
1. Fix Bugs!
2. Clean up Layout
3. Make the entries in the output clickable, so we don't have to have the "View" Button
4. Change code so we don't have to have the Column names for the drop down box hardcoded in
"""

import tkinter as tk  # Import required modules
import sqlite3
import re
import time

# Sqlite3 Config #
db_fn = 'CustomerRecords.db' # Database Name
conn = sqlite3.connect(db_fn)  # Globally defines database connection
data = []  # SQL Rows go here
page = 0  # Start from SQL OFFSET 0

def strip(self):
    """Strips illegal Characters from Input

    Strips out all characters except A-Z, a-z, 0-9, '-', '/'
    Prevents potential dataloss from potential SQL Injection
    """

    strpName = re.sub(r'[^a-zA-Z0-9\-/]', r'', self)
    return strpName  # Returns striped input so it can be used


def showOutput(page):
    """Produces SQL Output on Button Press

    Executes SQL Statement, outputs results as a Grid.
    Enables an SQL Search on an SQLite3 Database.
    """

    tstart = time.clock()  # Start Execution Time
    data = []
    rowPos = 5  # Grid Layout Row Position
    gridPos = 0  # Grid Position
    rowNum = 0  # Grid Row Number
    rowid = []  # SQL Row IDs
    cursor = conn.cursor()
    page = page  # Question: Is this even doing anything?
    querycount = "SELECT count(*) from details WHERE %s LIKE '%s';" % (sqlStr.get(), strip(sqlEntry.get())) #Not in Use
    query = "SELECT * FROM details WHERE %s LIKE '%s' ORDER BY id LIMIT 10 OFFSET %d;" % (  # SQL Query to execute
        sqlStr.get(), strip(sqlEntry.get()), page)
    cursor.execute(str(query))
    columns = next(zip(*cursor.description))  # Retrieves Column Names from Table
    rows = cursor.fetchall()  # Fetches all rows

    for col in columns:  # for loop adds in the column names in output grid
        colname = tk.Entry(mgui)
        colname.insert(tk.END, "  %s  " % (col))  # Inserts Column names to Grid
        colname.configure(state="disabled", text=col)  # Changes Entry to Read-Only
        colname.grid(row=4, column=int(gridPos), padx=4)
        gridPos +=1

    for row in rows:  # For each row in table: do
        colgridPos = 0
        id = ""  # Resets ID for each row in table
        for column in row:  # For each Column, insert data into tkinter Entry Widget
            rowcolname = tk.Entry(mgui)
            rowcolname.insert(tk.END, "%s" % (column))  # Inserts SQL Data into Grid
            rowcolname.grid(row=int(rowPos), column=int(colgridPos), padx=2)
            rowcolname.configure(state="disabled")
            colgridPos += 1
        id = str(row[0])
        rowid.append(id)
        data.append(row)
        tk.Button(mgui, text="View", command=lambda id=id: sqlPopup(id)).grid(column=6, row=int(rowPos), padx=4)
        rowNum += 1  # End of each for loop, adds an extra row
        rowPos += 1
    if len(rows) >= 10:  # if more than 10 results: show next button
        tk.Button(mgui, text="Back", command=lambda page=page: showOutput(page - 10)).grid(row=2, column=4, padx=4)
        tk.Button(mgui, text="Next", command=lambda page=page: showOutput(page + 10)).grid(row=2, column=6, padx=4)
    rowCount = len(rows)
    ttotal = time.clock() - tstart
    tk.Label(mgui, padx=2, text="Executed in %s Seconds" % (ttotal)).grid(row=16, padx=15, columnspan=3)
    tk.Label(mgui, padx=2, text="Total Rows: %s " % (rowCount)).grid(row=16, column=4)

def sqlPopup(id):
    """Shows SQL Results in popup Window

    Outputs the results in an additional popup window for easier access
    Arguments:
        id - SQL row ID passed from showOutput()
    """
    cursor = conn.cursor()
    query = "SELECT * FROM details WHERE id = '%s'" % id  # Select Row for ID
    cursor.execute(str(query))
    sqlrow = cursor.fetchall()
    popup = tk.Toplevel(mgui)
    popup.title("Details")
    mBox = tk.Text(popup, height=10, width=30)
    mBox.configure(state='normal')
    mBox.grid(row=1, column=1)
    mBox.insert(tk.END, "ID: %s\nFirst Name: %s\nLast Name: %s\nAddress: %s\nPhone: %s"
                %(sqlrow[0][0], sqlrow[0][1], sqlrow[0][2], sqlrow[0][3], sqlrow[0][4]))

    mBox.configure(state='disabled')


# ==== Tkinter Config ==== #
mgui = tk.Tk()
mgui.title("SQL Search")
sqlStr = tk.StringVar()
sqlEntry = tk.StringVar()
pageSub = 0
# ==== Entry Config ==== #
tk.Entry(mgui, textvariable=sqlEntry).grid(row=1, column=1)

# ==== Drop Down Menu Config ==== #
columns = ["id", "fname", "lname", "address", "phone"]
tk.OptionMenu(mgui, sqlStr, *columns).grid(row=1, column=2)
sqlStr.set(columns[0])  # Sets the Column names in the drop down box

# ==== Button Config ==== #
tk.Button(mgui, text='Submit', command=lambda: showOutput(pageSub), width=10).grid(row=1, column=3, sticky=tk.W, padx=8)
tk.Button(mgui, text='Close', command=mgui.quit, width=10).grid(row=1, column=4, sticky=tk.E, padx=8)

# ==== Label Config ==== #
tk.Label(mgui, text="SQL Test\n").grid(row=0)
tk.Label(mgui, text="Enter SQL Search: ").grid(row=1, column=0)
tk.Label(mgui, text="\n").grid(row=2)

if __name__ == "__main__":  # Runs the Tkinter App
    mgui.mainloop()
