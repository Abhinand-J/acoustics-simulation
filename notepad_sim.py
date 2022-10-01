import math
​
duration = 1 #in seconds
delta = 0.0001 #in seconds
​
size = 10 #in meters
walls = []
​
numRays = 100 #number of rays emanating from source
source = [5, 5] #must be INSIDE (not on wall) of box
​
#original intensity is ~ 100 dB (aka 2 Pascals), which is *slightly* louder than being next to a full symphony orchestra
originalIntensity = 200 #in centi-pascals (10^-2 pascals)
#minimum intensity is ~ 20 dB (aka 0.0002 Pascals), which is about the loudness of a whisper 5 ft away
minimumIntensity = 0.02 #in centi-pascals (10^-2 pascals)
​
VEL = 340 #in meters/second
​
distanceTraveled = VEL * delta #in meters
​
wCoeff = 0.9
rCoeff = 0.1
​
measure = [4, 3]
​
#measuredSound[time][ray][angle/intensity] = angle/intensity of particular ray at particular time
rawLeftSound = []
rawRightSound = []
​
rawInArea = []
​
#basic three walls
walls.append([])
walls[-1].append([0, 0])
walls[-1].append([0, size])
walls.append([])
walls[-1].append([0, 0])
walls[-1].append([size, 0])
walls.append([])
walls[-1].append([0, size])
walls[-1].append([size, size])
​
#rough surface
walls.append([])
walls[-1].append([size - 1, size/2])
walls[-1].append([size, 0])
walls.append([])
walls[-1].append([size - 1, size/2])
walls[-1].append([size, size])
​
listOfRays = []
angleIncrement = 2*math.pi / numRays
for index in range(numRays):
    angle = index * angleIncrement
    listOfRays.append([source[0], source[1], angle, originalIntensity])
​
def inLeft(x, y):
    if measure[0] - 0.1 <= x <= measure[0]:
        if measure[1] - 0.1 <= y <= measure[1] + 0.1:
            return True
    return False
​
def inRight(x, y):
    if measure[0] <= x <= measure[0] + 0.1:
        if measure[1] - 0.1 <= y <= measure[1] + 0.1:
            return True
    return False
​
def inVoid(x, y):    
    for wallPos in walls[3::]:
        xDiff = (wallPos[1][0] - wallPos[0][0])
        yDiff = (wallPos[1][1] - wallPos[0][1])
        if wallPos[0][1] <= y <= wallPos[1][1] or wallPos[0][1] >= y >= wallPos[1][1]:
            if xDiff == 0:
                if x > wallPos[0][0]:
                    return True
                return False
            wallSlope = yDiff / xDiff
            if x > ((y - wallPos[0][1]) / wallSlope + wallPos[0][0]):
                return True
    return False
​
def inBox(x, y):
    if 0 <= x <= size:
        if 0 <= y <= size:
            if inVoid(x, y) == False:
                return True
    return False
​
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
​
# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
​
def isIntersection(currentPos, newPos, wallLine):
    if intersect(currentPos, newPos, wallLine[0], wallLine[1]) == True:
        if math.dist(currentPos, lineIntersection([currentPos, newPos], wallLine)) == 0:
            return False
        return True
    return False
​
True
def inBetween(point, endpoint1, endpoint2): #corners are considered places
    if endpoint1[0] <= point[0] <= endpoint2[0] or endpoint1[0] >= point[0] >= endpoint2[0]:
        if endpoint1[1] <= point[1] <= endpoint2[1] or endpoint1[1] >= point[1] >= endpoint2[1]:
            return True
    return False
​
def lineIntersection(positions, wallLine):
    xdiff = (positions[0][0] - positions[1][0], wallLine[0][0] - wallLine[1][0])
    ydiff = (positions[0][1] - positions[1][1], wallLine[0][1] - wallLine[1][1])
​
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
​
    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
​
    d = (det(*positions), det(*wallLine))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
​
(10.25, -0.0)
def reflectPoint(x1, y1, wallLine):    
    x2 = wallLine[0][0]
    y2 = wallLine[0][1]
    
    x3 = wallLine[1][0]
    y3 = wallLine[1][1]
    
    if (x3 - x2) == 0:
        return 2*x2 - x1, y1
    if (y3 - y2) == 0:
        return x1, 2*y2 - y1
    m = (y3 - y2) / (x3 - x2)
    c = (x3*y2 - x2*y3) / (x3 - x2)
    
    d = (x1 + (y1 - c)*m) / (1 + m*m)
    
    x4 = 2*d - x1
    y4 = 2*d*m - y1 + 2*c
    
    return x4, y4
​
def getAngle(intersection, point):
    ang =  math.atan2(point[1] - intersection[1], point[0] - intersection[0])
    if ang >= 0:
        return ang
    else:
        return 2*math.pi + ang
    
def incrementRay(ray, i):
    currentPos = [ray[0], ray[1]]
    angle = ray[2]
    intensity = ray[3]
    newX = distanceTraveled*math.cos(angle) + ray[0]
    newY = distanceTraveled*math.sin(angle) + ray[1]
    iteration = 0
    while inBox(newX, newY) != True:
        if iteration > 2:
            print("iteration: " + str(iteration))
            return []
        closestWall = []
        wallDist = 10000000 #really big number so it goes down next time
        intersection = [0, 0]
        for wallLine in walls:
            if isIntersection(currentPos, [newX, newY], wallLine):
                intersect = lineIntersection([currentPos, [newX, newY]], wallLine)
                distance = math.dist(currentPos, intersect)
                if distance < wallDist:
                    closestWall = wallLine
                    wallDist = distance
                    intersection = intersect
        if closestWall == []:
            print(ray)
            print(currentPos)
            print(str(newX) + " " + str(newY))
            print(i)
            raise Exception("closestWall is empty despite inBox stating newPos is outside box")
            
        #found closest wall that the ray reflects off of
        currentPos = intersection
        newX, newY = reflectPoint(newX, newY, closestWall)
        angle = getAngle(intersection, [newX, newY])
        if closestWall in walls[:3:]:
            intensity *= wCoeff
        else:
            intensity *= rCoeff
        iteration += 1
    return [newX, newY, angle, intensity]    
​
for j in range(int(duration/delta)):
    print(j)
    rawLeftSound.append([])
    rawRightSound.append([])
    rawInArea.append([])
    toDelete = []
    for i in range(len(listOfRays)):
        listOfRays[i] = incrementRay(listOfRays[i], i) #ray is: [x, y, angle, intensity]
        if listOfRays[i] == []:
            print("adding to toDelete")
            toDelete.append(i)
            continue
        if inLeft(listOfRays[i][0], listOfRays[i][1]):
            rawLeftSound[-1].append([listOfRays[i][2], listOfRays[i][3]])
        if inRight(listOfRays[i][0], listOfRays[i][1]):
            rawRightSound[-1].append([listOfRays[i][2], listOfRays[i][3]])
        if inLeft(listOfRays[i][0], listOfRays[i][1]) or inRight(listOfRays[i][0], listOfRays[i][1]):
            rawInArea[-1].append([listOfRays[i][2], listOfRays[i][3]])
    for i in toDelete:
        listOfRays.pop(i)
        
leftSounds = []
rightSounds = []
bothSounds = []
def parse(sounds):
    ans = []
    for time in range(len(sounds)):
        if sounds[time] != []:
            ans.append(sounds[time])
            ans[-1].append(time)
    return ans
​
leftSounds = parse(rawLeftSound)
rightSounds = parse(rawRightSound)
bothSounds = parse(rawInArea)
​

def measure(sounds):
    ans = []
    for time in range(len(sounds)):
        if len(sounds[time]) > 2:
            x = 0
            y = 0
            for ray in range(len(sounds[time]) - 1):
                x += math.cos(sounds[time][ray][0])*sounds[time][ray][1]
                y += math.sin(sounds[time][ray][0])*sounds[time][ray][1]
            angle = math.atan2(y, x)
            intensity = math.dist([0, 0], [x, y])
            if intensity > 200:
                intensity = 200
            elif intensity < minimumIntensity:
                intensity = 0
            ans.append([angle, intensity, sounds[time][-1]])
        else:
            intensity = sounds[time][0][1]
            if intensity < minimumIntensity:
                intensity = 0
            ans.append([sounds[time][0][0], intensity, sounds[time][-1]])
    return ans
​
left = measure(leftSounds)
right = measure(rightSounds)
both = measure(bothSounds)

def finish(array):
    ans = []
    for i in array:
        if i[1] != 0:
            ans.append(i)
    return ans

left = finish(left)
right = finish(right)
both = finish(both)

print(both)