import sys
import re


# YOUR CODE GOES HERE
class Edge:
    def __init__(self, end1, end2):
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
        if (s.name != sToBeRemoved):
            newStreets.append(s)
    return newStreets


'''
def removeVertices(oldVertices, sToBeRemoved):

    targetSPs = sToBeRemoved.getSP()
    targetVertices = []

    for sp in targetSPs:
        targetVertices.append(sp.end1)
        targetVertices += sp.intersect
    targetVertices.append(targetSPs[-1].end2)

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
'''


def turnToTuple(stringName):
    stripParenthesis = stringName.strip('()')
    number = stripParenthesis.split(',')
    return tuple(map(int, number))


def checkOnSegment(a, b, c):
    if (a[0] - b[0]) * (c[1] - b[1]) == (c[0] - b[0]) * (a[1] - b[1]):
        if a[0] <= c[0] <= b[0] or a[0] >= c[0] >= b[0]:
            return c
    else:
        return None


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

    # if parallel
    if denominator == 0:

        if (sp1.end1 == sp2.end1 and sp1.end2 == sp2.end2) or (sp1.end1 == sp2.end2 and sp1.end2 == sp2.end1):
            return None
        '''
        if sp1.end1 == sp2.end1 or sp1.end1 == sp2.end2:
            return sp1.end1
        elif sp1.end2 == sp2.end1 or sp1.end2 == sp2.end2:
            return sp1.end2
        '''

        if checkOnSegment(sp1.end1, sp1.end2, sp2.end1) and checkOnSegment(sp1.end1, sp1.end2, sp2.end2):
            return [sp2.end1, sp2.end2]
        elif checkOnSegment(sp2.end1, sp2.end2, sp1.end1) and checkOnSegment(sp2.end1, sp2.end2, sp1.end2):
            return [sp1.end1, sp1.end2]
        elif checkOnSegment(sp1.end1, sp1.end2, sp2.end1) and checkOnSegment(sp2.end1, sp2.end2, sp1.end2):
            return [sp2.end1, sp1.end2]
        elif checkOnSegment(sp1.end1, sp1.end2, sp2.end1) and checkOnSegment(sp2.end1, sp2.end2, sp1.end1):
            return [sp2.end1, sp1.end1]
        elif checkOnSegment(sp1.end1, sp1.end2, sp2.end2) and checkOnSegment(sp2.end1, sp2.end2, sp1.end2):
            return [sp2.end2, sp1.end2]
        elif checkOnSegment(sp1.end1, sp1.end2, sp2.end2) and checkOnSegment(sp2.end1, sp2.end2, sp1.end1):
            return [sp2.end2, sp1.end1]

        elif checkOnSegment(sp2.end1, sp2.end2, sp1.end1) and checkOnSegment(sp1.end1, sp1.end2, sp2.end1):
            return [sp1.end1, sp2.end1]
        elif checkOnSegment(sp2.end1, sp2.end2, sp1.end1) and checkOnSegment(sp1.end1, sp1.end2, sp2.end2):
            return [sp1.end1, sp2.end2]
        elif checkOnSegment(sp2.end1, sp2.end2, sp1.end2) and checkOnSegment(sp1.end1, sp1.end2, sp2.end1):
            return [sp1.end2, sp2.end1]
        elif checkOnSegment(sp2.end1, sp2.end2, sp1.end2) and checkOnSegment(sp1.end1, sp1.end2, sp2.end2):
            return [sp1.end2, sp2.end2]

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
                if type(intersection) == list:
                    sp1.addIntersect(intersection[0])
                    sp1.addIntersect(intersection[1])

                    sp2.addIntersect(intersection[0])
                    sp2.addIntersect(intersection[1])

                else:
                    sp1.addIntersect(intersection)
                    sp2.addIntersect(intersection)

                    # print("add: " + str(intersection) + " to sp1")
                    # print("add: " + str(intersection) + " to sp2")

                intersectionList.append(intersection)

    return intersectionList


def main():
    VNum = 0
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    streets = []
    while True:
        line = sys.stdin.readline()
        command = line.split()[0]

        try:
            # no space between command and street name
            if len(command) != 1:
                raise Exception("missing space between command")

            if command != "g" and command != "r" and command != "a" and command != "c":
                raise Exception("Error: Incorrect input format")

            if command == "g":

                VNum = 0

                if len(line.split()) > 1:
                    raise Exception("redundant input for command g")

                # print("num of st: " + str(len(streets)))
                # calculate vertices

                vertices = []
                edges = []

                for s in streets:
                    for sp in s.getSP():
                        # get all intersections cleared
                        sp.intersect = []

                for i in range(len(streets)):
                    # check intersections between two streets
                    for j in range(i):
                        IntersectBetweenStreets(streets[i], streets[j])

                for s in streets:
                    # print("entered new street!: " + s.name)
                    for sp in s.getSP():
                        # print("entered new sp!")
                        verticesInSP = sp.intersect
                        # if there are not any intersections on sp
                        '''
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
                        '''
                        if verticesInSP:

                            vTemp = []
                            # add all vertices into temporary
                            for x in verticesInSP:
                                # type of x is Vertex!!!
                                # print("x type:" + str(type(x)))
                                vertex = Vertex(x)
                                # print("vertex type:" + str(type(vertex.getCo())))
                                vertex.addName(str(VNum))
                                VNum += 1

                                # print("vertex :" + str(vertex.getCo()[0]) + " " + str(vertex.getCo()[1]))
                                # print("vertex type:" + str(type(vertex.getCo())))
                                # print("vertex between ends: name is " + str(vertex.getName()) + " co is: " + str(vertex.getCo()))
                                vTemp.append(vertex)

                            v_left = Vertex(sp.end1)
                            v_left.addName(str(VNum))
                            VNum += 1
                            vTemp.append(v_left)
                            # print("vertex of end1 is " + str(v_left.getName()) + "co is: " + str(v_left.getCo()))

                            v_right = Vertex(sp.end2)
                            v_right.addName(str(VNum))
                            VNum += 1
                            vTemp.append(v_right)
                            # print("vertex of end2 is " + str(v_right.getName()) + "co is: " + str(v_right.getCo()))

                            # vertical line
                            if sp.end1[0] == sp.end2[0]:
                                # sort all vertices by second number
                                # print("vertical!\n")
                                v_sorted = sorted(vTemp, key=lambda v: v.getCo()[1])
                            # horizontal line
                            elif sp.end1[1] == sp.end2[1]:
                                # print("horizontal!\n")
                                # sort all vertices by first number
                                v_sorted = sorted(vTemp, key=lambda v: v.getCo()[0])
                            else:
                                # print("slope!\n")
                                v_sorted = sorted(vTemp, key=lambda v: v.getCo()[1])

                            for i in range(len(v_sorted) - 1):
                                if v_sorted[i + 1].getCo() == v_sorted[i].getCo():
                                    v_sorted[i + 1].name = v_sorted[i].name

                            # if any vertex in vTemp is the same as previous, change is name
                            # print("reached before here!")
                            for v_target in vertices:
                                # print("reached in v_target loop!")
                                for v in v_sorted:
                                    # print("reached in v_sorted loop!")
                                    # print("compare: " + str(v.getCo()) + " and " + str(v_target.getCo()))
                                    if v.getCo() == v_target.getCo():
                                        # print("change name! to " + v_target.name)
                                        v.name = v_target.name
                                    # print(v.name + str(v.getCo()))

                            '''
                            new_sorted = []
                            new_co = []
                            for i in range(len(v_sorted) - 1):
                                if v_sorted[i].getCo() not in new_co:
                                    new_co.append(v_sorted[i].getCo())
                                    new_sorted.append(v_sorted[i])
                            v_sorted = new_sorted
                            '''

                            # loop until the second last vertex
                            for i in range(len(v_sorted) - 1):
                                if (v_sorted[i].getCo() != v_sorted[i + 1].getCo()):
                                    e = [v_sorted[i].getName(), v_sorted[i + 1].getName()]
                                    edges.append(e)

                            vertices += v_sorted

                print("V = {")
                # print("length of vertices: " + str(len(vertices)))
                v_printedIndex = []
                for v in vertices:
                    if int(v.getName()) not in v_printedIndex:
                        print("  " + v.getName() + ":", end=' ')
                        print(' (' + '{0:.2f}'.format(v.getCo()[0]) + ',' + '{0:.2f}'.format(v.getCo()[1]) + ')')
                        v_printedIndex.append(int(v.getName()))
                    # print("\ntype of v is: " + str(type(v)))
                print("}")

                print("E = {")
                e_printedEdges = []
                for e in edges:
                    if e not in e_printedEdges:
                        print("  <" + str(e[0]) + "," + str(e[1]) + ">", end='')
                        e_printedEdges.append(e)

                        if edges.index(e) != len(edges) - 1:
                            print(",")
                        else:
                            print("\n", end='')
                print("}")
            else:
                m = re.search(r'"([^"]*)"', line)
                streetName = ""

                left = line.count("(")
                right = line.count(")")

                if left != right:
                    raise Exception("missing or redundant brackets")

                if m:
                    streetName = m.group(1)
                    # print("Street Name is " + streetName)
                else:
                    if line.count("\"") == 0:
                        raise Exception("missing street name")
                    else:
                        raise Exception("missing quotation marks")

                if line.count("\"") > 2:
                    raise Exception("redundant quotation marks")

                # check validity of streetName
                check = streetName.replace(" ", "")
                if not all(char.isalpha() for char in check):
                    raise Exception("invalid street name.")

                # print("Street Name is now " + streetName)

                coordinates = re.findall(r'\(.*?\)', line)
                # print(coordinates)

                if command == 'r':
                    # print("entered R!")

                    found = 0
                    for s in streets:
                        if s.name == streetName.lower():
                            found = 1
                    if not found:
                        raise Exception("invalid input: Street not found.")

                    if coordinates:
                        raise Exception("invalid input: redundant coordinates for command r")

                    targetStreet = None
                    for x in streets:
                        if x.name == streetName.lower():
                            targetStreet = x
                            break

                    # vertices = removeVertices(vertices, targetStreet)
                    streets = removeStreet(streets, streetName.lower())
                else:
                    # add or change streets
                    lineWithoutName = line.split("\"" + streetName + "\"")

                    if line.count("\"(") > 0:
                        raise Exception("missing space after street name")

                    if left == 0:
                        raise Exception("No brackets")

                    if len(coordinates) != left:
                        raise Exception("Missing or redundant brackets")

                    for c in coordinates:
                        x = turnToTuple(c)
                        if len(x) != 2:
                            raise Exception("invalid vertex")

                    if command == 'a':

                        s = Street(streetName.lower())

                        for xs in streets:
                            if xs.name == streetName.lower():
                                raise Exception("invalid input: Street exists.")

                        if len(coordinates) < 2:
                            raise Exception("invalid input: a street has at lease two vertices.")

                        if len(coordinates) > len(set(coordinates)):
                            raise Exception("invalid input: repetitive vertices.")

                        # all points except for the last one
                        for x in coordinates[:-1]:
                            sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                            s.append(sp)

                        streets.append(s)


                    elif command == 'c':

                        # vertices = removeVertices(vertices, targetStreet)

                        if len(coordinates) < 2:
                            raise Exception("invalid input: a street has at lease two vertices.")

                        if len(coordinates) > len(set(coordinates)):
                            raise Exception("invalid input: repetitive vertices.")

                        found = 0
                        for x in streets:
                            if x.name == streetName.lower():
                                found = 1
                        if found == 0:
                            raise Exception("Street not found.")

                        streets = removeStreet(streets, streetName.lower())

                        # the street to be modified
                        s = Street(streetName.lower())
                        for x in coordinates[:-1]:
                            sp = StreetPart(turnToTuple(x), turnToTuple(coordinates[coordinates.index(x) + 1]))
                            s.append(sp)

                        streets.append(s)

                # print('read a line:', line)
        except Exception as e:
            print("Error: " + str(e))
    # print('Finished reading input')

    # sp1 = StreetPart((0,0), (0,10))
    # sp2 = StreetPart((4,2), (4,8))

    # print(checkIntersect(sp1,sp2))

    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
