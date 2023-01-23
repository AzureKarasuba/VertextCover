import sys
import re

# YOUR CODE GOES HERE

class StreetPart:
    # This class is used to store parts of streets that are separated by vertices
    def __init__(self,end1,end2,intersect = []):
        self.intersect = None
        self.end1 = end1
        self.end2 = end2
        
    def addIntersect(self,coordinate):
        self.intersect.append(coordinate)

    def __str__(self):
        return str(self.end1) + " " + str(self.end2)

class Street:
    # This class refers to the Street as a whole
    def __init__(self,name):
        self.partList = []
        self.name = name
    
    def append(self,sp):
        self.partList.append(sp)

    def __str__(self):
        return str(self.partList)


def removeStreet(oldStreets, sToBeRemoved):
    newStreets = []
    for s in oldStreets:
        print (s.name)
        print (sToBeRemoved)
        if (s.name != sToBeRemoved):
            newStreets.append(s)
    return newStreets

def turnToTuple(stringName):
    stripParenthesis = stringName.strip('()')
    number = stripParenthesis.split(',')
    return tuple(map(int,number))

def read():

    # create a list of Street
    streets = []
    while True:
        line = sys.stdin.readline()
        command = line[0]

        if command == "g":
            break
        else:
            m = re.search(r'"([^"]*)"', line)
            streetName = ""

            if m:
                streetName = m.group(1)
                print("Street Name is " + streetName)

            print("Street Name is now " + streetName)

            if(command == 'r'):
                print ("entered R!")
                streets = removeStreet(streets, streetName)
            else:
                lineWithoutName = line.split("\"" + streetName + "\"")
                coordinates = lineWithoutName[1].split()
                print(coordinates)
                if command == 'a':
                    print("entered A!")
                    s = Street(streetName)

                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x),turnToTuple(coordinates[coordinates.index(x)+1]))
                        s.append(sp)
                    streets.append(s)

                elif command == 'c':
                    print("entered C!")
                    streets = removeStreet(streets,streetName)
                    if(streets == []):
                        print ("\nStreets is now empty!\n")
                    # the street to be modified
                    s = Street(streetName)
                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)
                    streets.append(s)

            print('read a line:', line)
    print('Finished reading input')
    for s in streets:
        print(s.name)
        for sp in s.partList:
            print (sp.end1)

def main():


    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    read()

    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
