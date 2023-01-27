import sys
import re

# YOUR CODE GOES HERE

class StreetPart:
    intersect = None
    end1 = ()
    end2 = ()
    # This class is used to store parts of streets that are separated by vertices
    def __init__(self, end1, end2):
        self.intersect = None
        self.end1 = end1
        self.end2 = end2
        
    def addIntersect(self,coordinate):
        self.intersect.append(coordinate)

    def __str__(self):
        return str(self.end1) + " " + str(self.end2)

class Street:
    # This class refers to the Street as a whole
    spList = []
    name = ""

    def __init__(self, name):
        self.spList = []
        self.name = name
    
    def append(self, sp):
        self.spList.append(sp)

    def getSP(self):
        return self.spList

    def __str__(self):
        return str(self.spList)


def removeStreet(oldStreets, sToBeRemoved):
    newStreets = []
    for s in oldStreets:
        print (s.name)
        print (sToBeRemoved)
        if (s.name != sToBeRemoved):
            newStreets.append(s)
    return newStreets

def removeVertices(oldVertices, sToBeRemoved):

    print("old Vertices: " + str(oldVertices))

    targetSPs = sToBeRemoved.getSP()
    targetVertices = []

    for sp in targetSPs:
        targetVertices.append(sp.end1)
    targetVertices.append(targetSPs[-1].end2)

    print("target: " + str(targetVertices))

    return [x for x in oldVertices if x not in targetVertices]


def turnToTuple(stringName):
    stripParenthesis = stringName.strip('()')
    number = stripParenthesis.split(',')
    return tuple(map(int,number))

def checkIntersect(sp1,sp2):

    sp1end1_x = sp1.end1[0]
    sp1end1_y = sp1.end1[1]
    sp1end2_x = sp1.end2[0]
    sp1end2_y = sp1.end2[1]

    sp2end1_x = sp2.end1[0]
    sp2end1_y = sp2.end1[1]
    sp2end2_x = sp2.end2[0]
    sp2end2_y = sp2.end2[1]

    denominator = (sp2end2_y - sp2end1_y) * (sp1end2_x - sp1end1_x) - (sp2end2_x - sp2end1_x) * (sp1end2_y - sp1end1_y)
    if denominator == 0:
        return None

    u_sp1 = ((sp2end2_x - sp2end1_x) * (sp1end1_y - sp2end1_y) - (sp2end2_y - sp2end1_y) * (sp1end1_x - sp2end1_x))/ denominator
    u_sp2 = ((sp1end2_x - sp1end1_x) * (sp1end1_y - sp2end1_y) - (sp1end2_y - sp1end1_y) * (sp1end1_x - sp2end1_x))/ denominator

    if (u_sp1 < 0 or u_sp1 > 1) or (u_sp2 < 0 or u_sp2 > 1):
        return None

    intersect = sp1end1_x + u_sp1 * (sp1end2_x - sp1end1_x), sp1end1_y + u_sp1 * (sp1end2_y - sp1end1_y)

    #
    sp1.addIntersect(intersect)
    sp2.addIntersect(intersect)

    return sp1end1_x + u_sp1 * (sp1end2_x - sp1end1_x), sp1end1_y + u_sp1 * (sp1end2_y - sp1end1_y)

def read():

    # create a list of Street
    vertices = []
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

                targetStreet = None
                for x in streets:
                    if x.name == streetName:
                        targetStreet = x
                        break

                vertices = removeVertices(vertices, targetStreet)
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
                        vertices.append(turnToTuple(x))

                    vertices.append(turnToTuple(coordinates[-1]))
                    streets.append(s)

                elif command == 'c':
                    print("entered C!")

                    targetStreet = None
                    for x in streets:
                        if x.name == streetName:
                            targetStreet = x
                            break

                    vertices = removeVertices(vertices, targetStreet)
                    streets = removeStreet(streets,streetName)


                    if(streets == []):
                        print ("\nStreets is now empty!\n")
                    # the street to be modified
                    s = Street(streetName)
                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)
                        vertices.append(turnToTuple(x))

                    vertices.append(turnToTuple(coordinates[-1]))
                    streets.append(s)

            print('read a line:', line)
    print('Finished reading input')

    for x in vertices:
        print(x)

def main():


    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    read()
    #sp1 = StreetPart((0,0), (0,10))
    #sp2 = StreetPart((4,2), (4,8))

    #print(checkIntersect(sp1,sp2))



    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
