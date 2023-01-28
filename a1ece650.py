import sys
import re

global VNum
VNum = 0
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

    def addIntersect(self, name, coordinate):
        self.intersect.append(Vertex(name,coordinate))

    def __str__(self):
        return str(self.end1) + " " + str(self.end2)


class Vertex:
    coordinate = None
    name = ""

    def __init__(self, n, co):
        self.name = n
        self.coordinate = co

    def getName(self):
        return self.name

    def getCo(self):
        return self.getCo()


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
        print(s.name)
        print(sToBeRemoved)
        if (s.name != sToBeRemoved):
            newStreets.append(s)
    return newStreets


def removeVertices(oldVertices, sToBeRemoved):
    print("old Vertices: " + str(oldVertices))

    targetSPs = sToBeRemoved.getSP()
    targetVertices = []

    for sp in targetSPs:
        targetVertices.append(sp.end1)
        targetVertices += sp.intersect
    targetVertices.append(targetSPs[-1].end2)

    print("target: " + str(targetVertices))

    newVertices = []
    for v in oldVertices:
        flag = 0
        for t in targetVertices:
            # old vertex is in targetVertices
            if v.coordinate == t.coordinate:
                flag = 1
        if flag == 0:
            newVertices.append(v)

    return newVertices


def turnToTuple(stringName):
    stripParenthesis = stringName.strip('()')
    number = stripParenthesis.split(',')
    return tuple(map(int, number))


def checkIntersect(sp1, sp2):
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

    u_sp1 = ((sp2end2_x - sp2end1_x) * (sp1end1_y - sp2end1_y) - (sp2end2_y - sp2end1_y) * (
            sp1end1_x - sp2end1_x)) / denominator
    u_sp2 = ((sp1end2_x - sp1end1_x) * (sp1end1_y - sp2end1_y) - (sp1end2_y - sp1end1_y) * (
            sp1end1_x - sp2end1_x)) / denominator

    if (u_sp1 < 0 or u_sp1 > 1) or (u_sp2 < 0 or u_sp2 > 1):
        return None

    intersection = sp1end1_x + u_sp1 * (sp1end2_x - sp1end1_x), sp1end1_y + u_sp1 * (sp1end2_y - sp1end1_y)

    #
    # sp1.addIntersect(intersection)
    # sp2.addIntersect(intersection)

    return intersection


def IntersectBetweenStreets(s1, s2):
    intersectionList = []
    for sp1 in s1.getSP():
        firstNumber = 0
        for sp2 in s2.getSP():
            secondNumber = 0
            intersection = checkIntersect(sp1, sp2)
            if intersection is not None:
                v = Vertex(str("V" + str(VNum)),intersection)
                VNum += 1
                sp1.addIntersect(v)
                sp2.addIntersect(v)

                intersectionList.append(v)
            secondNumber += 1
        firstNumber += 1

    return intersectionList


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    vertices = []
    edges = []

    streets = []
    while True:
        line = sys.stdin.readline()
        command = line[0]

        if command == "g":
            # calculate vertices
            for i in range(len(streets) - 1):
                # check intersections between two streets
                vertices += IntersectBetweenStreets(streets[i], streets[i + 1])
            print("Vertices:{\n" )
            for v in vertices:
                print(v.getName() + ":")
                print(v.getCo() + "\n")
            print("}\n")

            # check edges on each streetPart of each street
            for s in streets:
                for sp in s:
                    verticesInSP = sp.intersect
                    verticesInSP = verticesInSP.add(sp.end1)
                    verticesInSP = verticesInSP.add(sp.end2)

                    # check if there exist any intersection between two end points
                    if len(verticesInSP) > 2:
                        # vertical line
                        if sp.end1[0] == sp.end2[0]:
                            # sort all vertices by second number
                            sorted(verticesInSP, key=lambda v: v.getCo()[1])

                        # horizontal line
                        elif sp.end1[1] == sp.end2[1]:
                            sorted(verticesInSP, key=lambda v: v.getCo()[0])
                        else:
                            sorted(verticesInSP, key=lambda v: v.getCo()[1])

            break
        else:
            m = re.search(r'"([^"]*)"', line)
            streetName = ""

            if m:
                streetName = m.group(1)
                print("Street Name is " + streetName)

            print("Street Name is now " + streetName)

            if (command == 'r'):
                print("entered R!")

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
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)

                        vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(x)))
                        VNum += 1

                    vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(coordinates[-1])))
                    VNum += 1
                    streets.append(s)

                elif command == 'c':
                    print("entered C!")

                    targetStreet = None
                    for x in streets:
                        if x.name == streetName:
                            targetStreet = x
                            break

                    vertices = removeVertices(vertices, targetStreet)
                    streets = removeStreet(streets, streetName)

                    if (streets == []):
                        print("\nStreets is now empty!\n")
                    # the street to be modified
                    s = Street(streetName)
                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)
                        vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(x)))
                        VNum += 1

                    vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(coordinates[-1])))
                    VNum += 1
                    streets.append(s)

            print('read a line:', line)
    print('Finished reading input')

    for x in vertices:
        print(x)
    # sp1 = StreetPart((0,0), (0,10))
    # sp2 = StreetPart((4,2), (4,8))

    # print(checkIntersect(sp1,sp2))

    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
