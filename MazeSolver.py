import random
import math

#####################################
##          Test Boards            ##
#####################################

testB = [[[(1,0)],[(0,2),(1,1)],[(0,1),(1,2)]],
         [[(0,0),(2,0)],[(0,1)],[(0,2),(2,2)]],
         [[(1,0),(2,1)],[(2,0),(2,2)],[(1,2),(2,1)]]]

testA = [[[(1,0)],[(1,1)]],
         [[(0,0),(1,1)],[(0,1),(1,0)]]]

##TestA
##+-+-+
##| | |
##+ + +
##|   |
##+-+-+

##First Test
##+--+--+--+--+--+--+--+--+--+--+
##|  |  |     |  |  |     |  |  |
##+--+  +--+--+--+  +--+--+--+--+
##|  |  |     |  |  |  |     |  |
##+--+--+--+--+--+--+--+--+--+--+
##|  |     |  |  |  |  |     |  |
##+--+--+--+  +  +--+--+--+--+--+
##|  |  |  |  |  |  |  |     |  |
##+--+--+--+--+  +--+--+--+  +  +
##|  |     |  |  |  |  |  |  |  |
##+--+--+--+--+--+--+--+--+--+--+
##|  |  |  |  |  |  |  |     |  |
##+--+--+--+--+  +--+--+--+  +--+
##|  |  |  |  |  |  |  |  |     |
##+  +--+--+  +  +--+--+--+--+  +
##|  |  |  |  |  |  |  |  |  |  |
##+--+  +  +--+--+--+  +--+--+  +
##|     |  |  |  |  |  |  |  |  |
##+--+  +--+--+  +--+--+--+--+  +
##|  |  |  |  |  |  |  |     |  |
##+--+--+--+--+--+--+--+--+--+--+


def printMaze(edgeList, start = (0,0), goal = (0,0)):
    pHoriz = "##"
    for i in range(len(edgeList[0])):
        pHoriz += "####"
    print(pHoriz)
    pHoriz = ""
    pVert = ""

    currentEdges = []
    for x in range(len(edgeList)):
        pVert += "##"
        pHoriz += "##"
        for y in range(len(edgeList[x])):
            for z in range(len(edgeList[x][y])):
                currentEdges.append(edgeList[x][y][z])
##            if ((x,y) == goal):
##                pVert += " G|"
##                continue
##            if ((x,y) == start):
##                pVert += " S|"
##                continue
            if ((x,y+1) in currentEdges):
                pVert += "    "
            else:
                pVert += "  ##"
                
            if ((x+1,y) in currentEdges):
                pHoriz += "  ##"
            else:
                pHoriz += "####"
            currentEdges = []
        print(pVert)
        pVert = ""
        print(pHoriz)
        pHoriz = ""


#Creates a maze based on Prim's algorithm
#We use a fringe and add based on which element is the best to reach our goal
#Initially, we used random weight, essentially, and we plan to move to
#
def PrimMazeRectangle(n,m,start = (0,0)):

    
    ##Creates a list of all the possible edges in the maze where each list at position
    ## X,Y contains all the possible moves from that node
    edgeList = []
    for x in range(n):
        edges = []
        for y in range(m):
            inside = []
            for i in [-1,1]:
                #Don't include indeces outside of the maze
                if (x + i < 0 or x + i == n):
                    pass
                else:
                    inside.append((x + i, y))
                
            for j in [-1,1]:
                #Don't include indeces outside of the maze
                if (y + j < 0 or y + j == m):
                    pass
                else:
                    inside.append((x, y + j))
            edges.append(inside)
        edgeList.append(edges)

    #Holds a list of actual edges being used for the maze
    maze = [[[]for row in range(m)] for x in range(n)]
        
##This was used initially to make sure nothing exceeded indeces and worked well enough
##Essentially, testing for the below algorithm
##    for x in range(len(edgeList)):
##        for y in range(len(edgeList[x])):
##            choice = random.randint(0,len(edgeList[x][y]) - 1)
##            inside = edgeList[x][y][choice]
##            
##            maze[x][y].append(inside)
##            maze[inside[0]][inside[1]].append((x,y))
##    print(maze)
##    printMaze(maze)

##Print out each edge in the edgeList line-by-line
##    for x in range(len(edgeList)):
##        for y in range(len(edgeList[0])):
##            print(edgeList[x][y])

    used = []
##    fringe = [(random.randint(0,n-1), random.randint(0,m-1))]
    fringe = [start]
    while (len(fringe) != 0) and len(used) != n*m - 1:
##        blah = random.randint(0, len(fringe) - 1)
        current = fringe[0]
            
        while current in used:
            fringe.pop(0)
##            blah = random.randint(0, len(fringe) - 1)
            current = fringe[0]
            
        fringe.pop(0)
        choice = random.randint(0,len(edgeList[current[0]][current[1]]) - 1)
        nextNode = edgeList[current[0]][current[1]][choice]
        
        #Pick a direction only if it isn't already visited
        while(nextNode in used):
            choice = random.randint(0,len(edgeList[current[0]][current[1]]) - 1)
            nextNode = edgeList[current[0]][current[1]][choice]
            
        maze[current[0]][current[1]].append(nextNode)
        maze[nextNode[0]][nextNode[1]].append(current)
        used.append((current[0],current[1]))
        
        #Make sure to avoid adding any nodes that have already been visited.
        for i in edgeList[current[0]][current[1]]:
            if i in used:
                pass
            else:
                fringe.append(i)
    printMaze(maze, (0,0), (n-1, m-1))

def PrimMazeCircle(diameter = 11):
    edgeList = [[[] for x in range(diameter)] for y in range(diameter)]
    radius = math.floor(diameter/2)
    a = radius
    b = radius
    EPSILON = 2.2

    for x in range(diameter):
        for y in range(diameter):
            if (x-a)**2 + (y-b)**2 - radius**2 <= EPSILON**2:
                edgeList[x][y].append((x,y))

    for x in range(diameter - 1):
        for y in range(diameter - 1):
            if len(edgeList[x][y]) == 1:
                edgeList[x][y].append((x - 1, y))
                edgeList[x][y].append((x, y - 1))
                edgeList[x][y].append((x + 1, y))
                edgeList[x][y].append((x, y + 1))
                

    #Holds a list of actual edges being used for the maze
    maze = [[[]for row in range(diameter)] for x in range(diameter)]

    

    printMaze(edgeList)
            
def PrimMazeTriangle(n,m):
    edgeList = [[[] for x in range(n)] for y in range(m)]
    lineStart = math.floor(m/2)
    lineEnd = math.floor(m/2)

    for x in range(n):
        for y in range(m):
            if y in range(lineStart, lineEnd):
                if y%2 == 0:
                    edgeList[x][y].append((x+1,y))
##                    edgeList[x+1][y].append((x,y))
                else:
                    edgeList[x][y].append((x,y-1))
                    edgeList[x][y].append((x,y+1))
                    edgeList[x][y].append((x+1,y))
##                    
##                    edgeList[x][y+1].append((x,y))
##                    edgeList[x+1][y].append((x,y))
##                    edgeList[x][y-1].append((x,y))
        if lineStart > 0:
            lineStart -= 1
        if lineEnd < m - 1:
            lineEnd += 1

    for x in range(len(edgeList)):
        print()
        for y in range(len(edgeList[x])):
            print(edgeList[x][y], end="")
    printMaze(edgeList)

    
    
PrimMazeRectangle(5,5,(0,0))
PrimMazeCircle(11)
PrimMazeTriangle(10, 20)

##First Prim Maze (10,10)
##+--+--+--+--+--+--+--+--+--+--+
##|                    |     |  |
##+--+  +--+--+--+  +  +  +  +  +
##|     |        |  |     |  |  |
##+--+--+--+--+  +  +--+  +  +  +
##|  |           |  |     |     |
##+  +  +--+  +  +  +--+--+--+  +
##|     |     |     |  |        |
##+--+--+--+  +--+--+  +--+--+  +
##|           |                 |
##+--+--+--+--+--+--+--+--+--+  +
##|  |     |           |        |
##+  +--+  +--+--+  +  +--+--+  +
##|              |  |        |  |
##+--+--+--+  +  +--+--+  +  +  +
##|        |  |  |        |     |
##+--+  +  +--+  +  +--+--+--+  +
##|  |  |           |  |        |
##+  +  +--+--+--+  +  +--+--+  +
##|     |           |           |
##+--+--+--+--+--+--+--+--+--+--+

##PrimMaze(20,20)   
##################################################################################
##  ##      ##                      ##      ##      ##      ##      ##      ##  ##
##  ######  ##  ######  ##########  ##  ##  ##  ##  ##  ##  ######  ##  ##  ##  ##
##  ##          ##      ##  ##      ##  ##      ##  ##  ##  ##          ##      ##
##  ##########  ##########  ######  ##  ######  ##  ######  ##########  ######  ##
##  ##          ##          ##      ##  ##      ##          ##          ##      ##
##  ##########  ######  ##  ######  ##  ######  ######  ##  ##########  ######  ##
##  ##          ##  ##  ##          ##  ##      ##      ##              ##  ##  ##
##  ##########  ##  ##############  ##  ######  ######################  ##  ##  ##
##  ##          ##          ##          ##  ##  ##                      ##  ##  ##
##  ######################  ##########  ##  ##########  ######  ######  ##  ##  ##
##          ##              ##          ##          ##  ##      ##      ##      ##
######  ##  ##########  ##  ##################  ##  ##################  ######  ##
##  ##  ##          ##  ##  ##      ##      ##  ##          ##      ##  ##      ##
##  ##  ##########  ##  ##  ######  ######  ##############  ######  ##  ######  ##
##  ##  ##          ##  ##  ##      ##                      ##      ##  ##  ##  ##
##  ##  ##########  ######  ######  ##  ##################  ######  ######  ##  ##
##  ##  ##  ##      ##                  ##  ##      ##              ##      ##  ##
##  ######  ##  ##  ##  ##############  ##  ######  ##############  ######  ##  ##
##  ##          ##      ##  ##          ##                  ##                  ##
##  ##  ######  ##########  ##########  ######  ##########  ##  ######  ######  ##
##  ##  ##      ##  ##              ##  ##      ##              ##      ##  ##  ##
##  ##########  ##  ##  ######  ##  ##  ##############################  ##  ##  ##
##          ##  ##  ##  ##  ##  ##  ##  ##                          ##  ##      ##
##########  ##  ##  ##  ##  ##  ##  ##########  ######  ######  ##  ##  ######  ##
##  ##          ##      ##      ##              ##      ##  ##  ##      ##      ##
##  ##  ##############################  ######  ######  ##  ##  ######  ######  ##
##  ##  ##          ##              ##  ##      ##  ##  ##  ##  ##      ##  ##  ##
##  ##############  ##############  ##  ######  ##  ######  ##########  ##  ##  ##
##                  ##      ##          ##  ##  ##  ##              ##  ##  ##  ##
######  ##########  ##  ##  ##############  ######  ##########  ##  ######  ##  ##
##      ##              ##          ##              ##          ##  ##      ##  ##
######  ##############  ##########  ##############  ##########  ##  ##  ##  ##  ##
##  ##  ##          ##  ##  ##                              ##  ##  ##  ##  ##  ##
##  ##########  ##  ##  ##  ##  ######  ######  ##########  ##  ##  ##  ##  ##  ##
##  ##      ##  ##  ##  ##      ##  ##  ##  ##  ##              ##  ##  ##  ##  ##
##  ##  ##  ##  ##  ##  ######  ##  ##  ##  ##  ##################  ##  ##  ##  ##
##  ##  ##  ##  ##      ##      ##  ##  ##      ##          ##      ##  ##  ##  ##
##  ######  ##########  ######  ##  ##################  ##  ##  ##  ##  ##  ##  ##
##                      ##      ##                      ##      ##      ##      ##
##################################################################################

###Creates a random maze, where there can be open spaces and enclosed 
##def randomMaze(n, m):
##
##    #Create an edge list that we can put into the 
##    maze = []
##    for x in range(n):
##        edges = []
##        for y in range(m):
##            inside = [(x,y)]
##            edges.append(inside)
##        maze.append(edges)
##        
##    adjPosition = ()
##    for i in range(n):
##        for j in range(m):
##            pass
##            
##            #Don't go up or left
##            if i == 0 and j == 0:
##                direction = random.randint(0,1)
##            #Don't go up
##            elif i == 0:
##                direction = random.choice([0,1,3])
##            #Don't go left
##            elif j == 0:
##                direction = random.randint(0,2)
##            #Don't go right or down
##            elif i == n - 1 and j == m - 1:
##                direction = random.randint(2,3)
##            #Don't go down
##            elif i == n - 1:
##                direction = random.randint(1, 3)
##            #Don't go right
##            elif j == m - 1:
##                direction = random.choice([0, 2, 3])
##            print(i,j, direction)
##            
##            #If 0 choose down
##            if direction == 0:
##                adjPosition = (min((i + 1), n-1), j)
##            #If 1 choose right
##            if direction == 1:
##                adjPosition = (i, min((j + 1), m-1))
##            #If 2 choose up
##            if direction == 2:
##                adjPosition = (max((i - 1), 0), j)
##            #if 3 choose left
##            if direction == 3:
##                adjPosition = (i, max((j - 1), 0))
##            print(adjPosition)
##            maze[i][j].append(adjPosition)
##    print(maze)
##    printMaze(maze)
##                
##randomMaze(10, 10)

##For figuring out an algorithm to design a circle
##http://stackoverflow.com/questions/22777049/how-can-i-draw-a-circle-in-a-data-array-map-in-python
