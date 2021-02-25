import re, time, datetime, random

# Enter Name & Date of Birth
# Generate 6 Character Password, must include binary conversion step
# Password must contain only upper, lower case, one number

passw = []
abc = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ" * 5
num = "0123456789"


def strip(self):
    strpName = re.sub(r'[^a-zA-Z\- ]', r'', self)  # Function to  strip unwanted characters
    return strpName


def name():
    try:
        print("Enter your Details\n")
        fName = strip(input("First Name: "))  # Uses strip() to strip invalid input
        lName = strip(input("Last Name: "))
        dob = input("Enter D.O.B(DD/MM/YYYY): ")
        time.strptime(dob, "%d/%m/%Y")  # Ensures a Valid Input D.O.B
        print("Full Name: ", fName, lName)
        print("Date of Birth: ", dob)
        yrAge = dob[6:]  # D.O.B Year
        mAge = dob[3:5]  # D.O.B Month
        totalYr = int(datetime.date.today().year) - int(yrAge)
        if int(datetime.date.today().month) > int(dob[3:5]):
            age = int(totalYr) + 1
        else:
            age = totalYr
        print("Age: ", age)
        for i in fName, lName, dob, age:
            bname = (','.join(map(bin, bytearray(str(i), 'ascii'))))
            bsplit = bname.split(",")
            one = 0
            zero = 0
            for x in bname:
                if "1" in x:
                    one += 1
                elif "0" in x:
                    zero += 1
            passw.append(abc[int(one)])
            passw.append(abc[int(zero)])
            # print("Total Ones: %s\nTotal Zeroes: %s" % (one, zero))
            # print("Total Ones: %s\nTotal Zeros: %s" % (one, zero))
        passwd = ''.join(passw)
        passwd2 = (passwd[:5] + random.choice(num))
        nameByte = fName, lName
        nameBin = (' '.join(map(bin, bytearray(str(nameByte), 'ascii'))))
        print("Password: %s" % passwd2)
        print("Binary Name: ", nameBin)
    except ValueError:
        print("Error: Invalid Date of Birth. Enter as DD/MM/YYYY (21/02/1990).")


if __name__ == "__main__":
    name()
