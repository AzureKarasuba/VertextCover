import sys
import re


# YOUR CODE GOES HERE
class Edge:
    def __init__(self,end1, end2):
        # datatype of end1 and end 2 is Vertex
        self.end1 = end1
        self.end2 = end2


class Vertex:

    def __init__(self, co):
        self.name = ""
        self.coordinate = co

    def addName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getCo(self):
        return self.coordinate

    def __eq__(self, other):
        return self.coordinate == other.coordinate

    def __getitem__(self, item):
        return self.coordinate[item]


class StreetPart:

    # This class is used to store parts of streets that are separated by vertices
    def __init__(self, end1, end2):
        self.intersect = []
        self.end1 = end1
        self.end2 = end2

    def addIntersect(self, coordinate):
        self.intersect.append(coordinate)

    def __str__(self):
        return str(self.end1) + " " + str(self.end2)


class Street:
    # This class refers to the Street as a whole

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
        for sp2 in s2.getSP():
            intersection = checkIntersect(sp1, sp2)
            if intersection is not None:
                # print("type of intersection in IBS: " + str(type(intersection)))

                # v = Vertex(intersection)
                sp1.addIntersect(intersection)
                sp2.addIntersect(intersection)

                intersectionList.append(intersection)

    return intersectionList


def main():
    global VNum
    VNum = 0
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    streets = []
    while True:
        line = sys.stdin.readline()
        command = line[0]

        if command == "g":
            # calculate vertices
            vertices = []
            edges = []

            for i in range(len(streets) - 1):
                # check intersections between two streets
                IntersectBetweenStreets(streets[i], streets[i + 1])

            for s in streets:
                for sp in s.getSP():
                    verticesInSP = sp.intersect
                    # if there are not any intersections on sp
                    if not verticesInSP:
                        print("between " + str(sp.end1) + " and " + str(sp.end2) + ", there isn't any intersection")
                        v_left = Vertex(sp.end1)
                        v_left.addName(str(VNum))
                        VNum += 1

                        v_right = Vertex(sp.end2)
                        v_right.addName(str(VNum))
                        VNum += 1

                        for v_target in vertices:
                            if v_left.getCo() == v_target.getCo():
                                v_left.name = v_target.name
                            if v_right.getCo() == v_target.getCo():
                                v_right.name = v_target.name

                        vertices.append(v_left)
                        vertices.append(v_right)
                    else:
                        print("between " + str(sp.end1) + " and " + str(sp.end2) + ", there is " + str(
                            len(verticesInSP)) + " intersection")
                        vTemp = []
                        # add all vertices into temporary
                        for x in verticesInSP:
                            # type of x is Vertex!!!
                            # print("x type:" + str(type(x)))
                            vertex = Vertex(x)
                            # print("vertex type:" + str(type(vertex.getCo())))
                            vertex.addName(str(VNum))
                            VNum += 1

                            print("vertex :" + str(vertex.getCo()[0]) + " " + str(vertex.getCo()[1]))
                            # print("vertex type:" + str(type(vertex.getCo())))
                            print("vertex between ends: name is " + str(vertex.getName()) + " co is: " + str(vertex.getCo()))
                            vTemp.append(vertex)

                        v_left = Vertex(sp.end1)
                        v_left.addName(str(VNum))
                        VNum += 1
                        vTemp.append(v_left)
                        print("vertex of end1 is " + str(v_left.getName()) + "co is: " + str(v_left.getCo()))

                        v_right = Vertex(sp.end2)
                        v_right.addName(str(VNum))
                        VNum += 1
                        vTemp.append(v_right)
                        print("vertex of end2 is " + str(v_right.getName()) + "co is: " + str(v_right.getCo()))

                        # vertical line
                        if sp.end1[0] == sp.end2[0]:
                            # sort all vertices by second number
                            print("vertical!\n")
                            v_sorted = sorted(vTemp, key=lambda v: v.getCo()[1])
                        # horizontal line
                        elif sp.end1[1] == sp.end2[1]:
                            print("horizontal!\n")
                            # sort all vertices by first number
                            v_sorted = sorted(vTemp, key=lambda v: v.getCo()[0])
                        else:
                            print("slope!\n")
                            v_sorted = sorted(vTemp, key=lambda v: v.getCo()[1])

                        # if any vertex in vTemp is the same as previous, change is name
                        for v_target in vertices:
                            for v in v_sorted:
                                if v.getCo() == v_target.getCo():
                                    v.name = v_target.name

                        new_sorted = []
                        for i in range(len(v_sorted) - 1):
                            if v_sorted[i].getCo()

                            # loop until the second last vertex
                        for i in range(len(v_sorted) - 1):
                            e = [v_sorted[i].getName(), v_sorted[i + 1].getName()]
                            print ("There is an edge between " +
                                   str(v_sorted[i].getName()) + " with co of: "+str(v_sorted[i].getCo()) + " and " +
                                   str(v_sorted[i + 1].getName()) + " with co of: " + str(v_sorted[i + 1].getCo()))

                            edges.append(e)
                            print(type(e))
                            print("e: " + str(e))
                        print("end!\n\n")
                        vertices += v_sorted

            print("Vertices:{\n")
            print("length of vertices: " + str(len(vertices)))
            v_printedIndex = []
            for v in vertices:
                if int(v.getName()) not in v_printedIndex:
                    print(v.getName() + ": " + str(v.getCo()) + ",\n")
                    v_printedIndex.append(int(v.getName()))
                # print("\ntype of v is: " + str(type(v)))
            print("}\n")

            print("Edges:{\n")
            for e in edges:
                print(str(e) + ",\n")
            print("}\n")
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

                # vertices = removeVertices(vertices, targetStreet)
                streets = removeStreet(streets, streetName)
            else:
                # add or change streets
                lineWithoutName = line.split("\"" + streetName + "\"")
                coordinates = lineWithoutName[1].split()
                print(coordinates)

                if command == 'a':
                    print("entered A!")
                    s = Street(streetName)

                    # all points except for the last one
                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)

                        # vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(x)))
                        # VNum += 1

                    # vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(coordinates[-1])))
                    # VNum += 1
                    streets.append(s)

                elif command == 'c':
                    print("entered C!")

                    '''
                    targetStreet = None
                    for x in streets:
                        if x.name == streetName:
                            targetStreet = x
                            break
                    '''

                    # vertices = removeVertices(vertices, targetStreet)
                    streets = removeStreet(streets, streetName)

                    if (streets == []):
                        print("\nStreets is now empty!\n")
                    # the street to be modified
                    s = Street(streetName)
                    for x in coordinates[:-1]:
                        sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                        s.append(sp)
                        # vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(x)))
                        # VNum += 1

                    # vertices.append(Vertex(str("V" + str(VNum)), turnToTuple(coordinates[-1])))
                    # VNum += 1
                    streets.append(s)

            print('read a line:', line)
    print('Finished reading input')

    # sp1 = StreetPart((0,0), (0,10))
    # sp2 = StreetPart((4,2), (4,8))

    # print(checkIntersect(sp1,sp2))

    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
