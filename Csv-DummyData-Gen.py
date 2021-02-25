## Python Script to Generate Details Csv
## id, name, fname, lname, address, phone

import random


names = []
firstNames = ["Justin", "John", "Peter", "Sam", "Amy", "Jessica",
              "David", "Jeremy", "Susie", "Kathleen", "Tom",
              "Robert", "James", "William", "Jack", "Noah",
              "Lucas", "Ethan", "Ruby", "Mia", "Sophie",
              "Emily", "Chloe", "Daniel", "Michael", "Sami",
              "Eric", "Kyle", "Jeren", "Mike", "Brendan", "Jo",
              "Tony", "Rachael", "Emily"]
lastNames = ["Smith","Doe","Peterson","Masterson","Johnson","Jones",
             "Brown", "Davies", "Anderson", "White", "Miller",
             "Wilson", "Thomas", "Harris", "Martin", "Thompson",
             "Lee", "Cook", "Morgan", "Bell", "Cooper", "Rege",
             "Treen", "Porse", "Mathers", "Sign", "Road", "Awer",
             "Jonhason", "Hanson", "Field", "Book", "Camper"]
addressNames = ["Station Street", "High Street", "Peters Road",
                "Victoria Crescent", "Fake Street", "Epper Road",
                "String Road", "Field Street", "Samma Street"]

csvout = open("names5.csv", "w")

def phnum():
    firstNum = "04"
    fullNum = []
    for i in range(1,8):
        numB = random.randrange(0,9)
        fullNum.append(numB)
        numB = ""
    numAll = ''.join(map(str, fullNum))
    return firstNum+numAll

id = 1

for i in range(1,51):
    rNum = random.randrange(0,9)
    name = ("%s,%s,%s,%s %s,%s" % (id, random.choice(firstNames), random.choice(lastNames),
        random.randrange(1,300), random.choice(addressNames), phnum()))
    names.append(name)
    id += 1

csvout.write("id, fname, lname, address, phone\n\n")
for x in names:
    print("%s" % (x))
    csvout.write("%s\n" % x)
csvout.close()
