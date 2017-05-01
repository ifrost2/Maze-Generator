import random
import math
import copy

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


##PRINT RECTANGULAR MAZE####################################################


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

##PRINT CIRCULAR MAZE####################################################

def printMazeCircle(edgeList, diameter):
    pHoriz = "##"
    pVert = ""
    for i in range(len(edgeList[0])):
        pHoriz += "####"
    print(pHoriz)
    pHoriz = ""

    currentEdges = []
    for x in range(len(edgeList)):
        pHoriz += "##"
        pVert += "##"
        for y in range(len(edgeList[x])):
            #know which edges are possible from the current position
            for z in range(len(edgeList[x][y])):
                currentEdges.append(edgeList[x][y][z])

            #If the current one is empty
            if len(edgeList[x][y]) == 0:
                pVert += "####"
                pHoriz += "####"
            else:
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


##PRINT TRIANGULAR MAZE####################################################
def printMazeTriangle(edgeList, n, m):
    pHoriz = "##"
    pVert = ""
    for i in range(len(edgeList[0])):
        pHoriz += "####"
    print(pHoriz)
    pHoriz = ""
    pAll = ""


    #Construct the maze printing from the bottom.
    currentEdges = []
    for x in reversed(range(len(edgeList))):
        for y in reversed(range(len(edgeList[x]))):
            #know which edges are possible from the current position
            for z in range(len(edgeList[x][y])):
                currentEdges.append(edgeList[x][y][z])

                
            #If the current one is empty
            if len(edgeList[x][y]) == 0:
                pVert = "####" + pVert
                pHoriz = "####" + pHoriz
            else:
                if ((x,y+1) in currentEdges):
                    pVert = "    " + pVert
                else:
                    pVert = "  ##" + pVert
                    
                if ((x+1,y) in currentEdges):
                    pHoriz = "  ##" + pHoriz
                else:
                    pHoriz = "####" + pHoriz
            
            currentEdges = []
            
        pAll = "##" + pVert + "\n" + "##" + pHoriz + "\n" + pAll
        pVert = ""
        pHoriz = ""
    print(pAll)

    
                
            

##MAKE A RECTANGULAR MAZE ###################################################
#Creates a maze based on Prim's algorithm
#We use a fringe and add based on which element is the best to reach our goal
#Initially, we used random weight, essentially, and we plan to move to
#Works with odd and even numbers
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

    used = []
    fringe = [start]
    #While there are still edges to be discovered and all of the
    #nodes have not been visited
    while (len(fringe) != 0) and len(used) != n*m - 1:
        current = fringe[0]

        #Don't visit a node that has already been added to the maze
        while current in used:
            fringe.pop(0)
            current = fringe[0]

        #Choose the initial nextNode  
        fringe.pop(0)
        choice = random.randint(0,len(edgeList[current[0]][current[1]]) - 1)
        nextNode = edgeList[current[0]][current[1]][choice]
        
        #Pick a direction only if it isn't already visited
        while(nextNode in used):
            choice = random.randint(0,len(edgeList[current[0]][current[1]]) - 1)
            nextNode = edgeList[current[0]][current[1]][choice]

        #Add the choice to used and update both in the maze for printing
        #purposes
        maze[current[0]][current[1]].append(nextNode)
        maze[nextNode[0]][nextNode[1]].append(current)
        used.append(current)
        
        #Make sure to avoid adding any nodes that have already been visited.
        for i in edgeList[current[0]][current[1]]:
            if i in used:
                pass
            else:
                fringe.append(i)
    printMaze(maze, (0,0), (n-1, m-1))


##MAKE A CIRCULAR MAZE ###################################################
##Works best if using odd numbers
def PrimMazeCircle(diameter = 11):
    edgeList = [[[] for x in range(diameter)] for y in range(diameter)]
    radius = math.floor(diameter/2)
    a = radius
    b = radius
    EPSILON = 2.2
    start = (0,0)

    #Add edges based on an algorithm
    #To not risk adding an edge outside of the circle, just put itself
    #in the edge list
    for x in range(diameter):
        for y in range(diameter):
            if (x-a)**2 + (y-b)**2 - radius**2 <= EPSILON**2:
                edgeList[x][y].append((x,y))
                if start == (0,0):
                    start = (x,y)

    #Make a list of all the edges possible in this graph
    for x in range(diameter):
        for y in range(diameter):
            if len(edgeList[x][y]) == 1:
                up = max(0, x-1)
                down = min(diameter-1, x+1)
                left = max(0, y-1)
                right = min(diameter-1, y+1)
                
                if up == x or len(edgeList[up][y]) == 0:
                    pass
                else:
                    edgeList[x][y].append((up, y))
                if down == x or len(edgeList[down][y]) == 0:
                    pass
                else:
                    edgeList[x][y].append((down, y))
                if right == y or len(edgeList[x][right]) == 0:
                    pass
                else:
                    edgeList[x][y].append((x, right))
                if left == y or len(edgeList[x][left]) == 0:
                    pass
                else:
                    edgeList[x][y].append((x, left))

                    
    #Holds a list of actual edges being used for the maze
    maze = [[[]for row in range(diameter)] for x in range(diameter)]

    usedEdges = []

    #Add all the unused edges to used to count towards the ending
    for x in range(len(edgeList)):
        for y in range(len(edgeList[x])):
            if len(edgeList[x][y]) == 0:
                usedEdges.append((edgeList[x][y], edgeList[x][y]))

    used = []       

    temp = copy.deepcopy(edgeList)
    #Have each element in the fringe keep track of where it came from
    fringe = [(start, (0,0))]
    while (len(fringe) != 0):
        current = fringe[0][0]

        #Don't add anything already in used or if it isn't in the circle
        while current in used or len(temp[current[0]][current[1]]) == 0:
            lastNode = fringe[0]
            fringe.pop(0)
            if len(fringe) == 0:
                break
            current = fringe[0][0]
            
        #If ever the fringe is 0
        #Connect the last node looked at to the node from which it was added
        if len(fringe) == 0:
            nextNode = lastNode[1]
            maze[current[0]][current[1]].append(nextNode)
            maze[nextNode[0]][nextNode[1]].append(current)
            used.append((current[0],current[1]))
            break
            
        #Store where the node came from in case every other node has been visited
        prevNode = fringe[0][1]
        fringe.pop(0)

        poss = temp[current[0]][current[1]]

        #Remove itself from possible choices
        if current in poss:
            poss.remove(current)

        #Pick a direction initially
        choice = random.randint(0,len(poss) - 1)
        nextNode = poss[choice]
        
        #Pick a direction only if it isn't already visited
        #Break out if all possibilities are already visited
        while(nextNode in used):
            poss.pop(choice)
            if len(poss) == 0:
                break
            choice = random.randint(0,len(poss) - 1)
            nextNode = poss[choice]

        #If ever we get to a point where the current node has no options
        #create an edge between it and the node it came from
        if len(poss) == 0:
               nextNode = prevNode
               
        #Add the edges and nodes to used so we avoid visiting them again
        maze[current[0]][current[1]].append(nextNode)
        maze[nextNode[0]][nextNode[1]].append(current)
        used.append(current)
        usedEdges.append((current, nextNode))
        
        #Make sure to avoid adding any nodes that have already been visited.
        for i in poss:
            if i in used:
                pass
            else:
                fringe.append((i,current))

    #Find where nodes went back and forth and finish connecting the
    #entire maze together
    leftovers = []
    for x in usedEdges:
        for y in usedEdges:
            if (x[0],x[1]) == (y[1],y[0]) and x != ([],[]):
                leftovers.append(x[0])

    #Makes sure that every possible move is made from these nodes
    #that essentially did nothing to ensure every node is reachable
    #(Not the best way of doing it but it works with very few extra
    #nodes added)
    for i in leftovers:
        current = i
        poss = edgeList[i[0]][i[1]]
        for j in range(len(poss)):
            nextNode = poss[j]
            if nextNode == current:
                pass
            else:
                maze[current[0]][current[1]].append(nextNode)
                maze[nextNode[0]][nextNode[1]].append(current)
                used.append(current)
                usedEdges.append((current, nextNode)) 

    #Print the maze
    printMazeCircle(maze, diameter)

##MAKE A TRIANGULAR MAZE ###################################################
## Works with odd and even numbers as m is always calculated to be odd
def PrimMazeTriangle(n):
    m = (2*n) - 1
    edgeList = [[[] for y in range(m)] for x in range(n)]
    lineStart = math.floor(m/2)
    lineEnd = math.floor(m/2)

    #Add only the current element to the edgeList initially
    #so we can check for lengths when adding all possibilities
    for x in range(n):
        for y in range(m):
            if y in range(lineStart, lineEnd) or (y == lineStart or y == lineEnd):
                edgeList[x][y].append((x,y))
        if lineStart > 0:
            lineStart -= 1
        if lineEnd < m - 1:
            lineEnd += 1


    #Make a list of all the edges possible in this graph
    for x in range(n):
        for y in range(m):
            if len(edgeList[x][y]) == 1:
                up = max(0, x-1)
                down = min(n-1, x+1)
                left = max(0, y-1)
                right = min(m-1, y+1)
                
                if up == x or len(edgeList[up][y]) == 0:
                    pass
                else:
                    edgeList[x][y].append((up, y))
                if down == x or len(edgeList[down][y]) == 0:
                    pass
                else:
                    edgeList[x][y].append((down, y))
                if right == y or len(edgeList[x][right]) == 0:
                    pass
                else:
                    edgeList[x][y].append((x, right))
                if left == y or len(edgeList[x][left]) == 0:
                    pass
                else:
                    edgeList[x][y].append((x, left))

    ##ESSENTIALLY USES COPY-PASTED CODE FROM THE PRIM CIRCLE
    #Holds a list of actual edges being used for the maze
    maze = [[[]for row in range(m)] for x in range(n)]

    usedEdges = []

    #Add all the unused edges to used to count towards the ending
    for x in range(len(edgeList)):
        for y in range(len(edgeList[x])):
            if len(edgeList[x][y]) == 0:
                usedEdges.append((edgeList[x][y], edgeList[x][y]))

    used = []       

    temp = copy.deepcopy(edgeList)
    #Have each element in the fringe keep track of where it came from
    fringe = [((0,math.floor(m/2)), (0,0))]
    while (len(fringe) != 0):
        current = fringe[0][0]

        #Don't add anything already in used or if it isn't in the circle
        while current in used or len(temp[current[0]][current[1]]) == 0:
            lastNode = fringe[0]
            fringe.pop(0)
            if len(fringe) == 0:
                break
            current = fringe[0][0]
            
        #If ever the fringe is 0
        #Connect the last node looked at to the node from which it was added
        if len(fringe) == 0:
            nextNode = lastNode[1]
            maze[current[0]][current[1]].append(nextNode)
            maze[nextNode[0]][nextNode[1]].append(current)
            used.append((current[0],current[1]))
            break
            
        #Store where the node came from in case every other node has been visited
        prevNode = fringe[0][1]
        fringe.pop(0)

        poss = temp[current[0]][current[1]]

        #Remove itself from possible choices
        if current in poss:
            poss.remove(current)

        #Pick a direction initially
        choice = random.randint(0,len(poss) - 1)
        nextNode = poss[choice]
        
        #Pick a direction only if it isn't already visited
        #Break out if all possibilities are already visited
        while(nextNode in used):
            poss.pop(choice)
            if len(poss) == 0:
                break
            choice = random.randint(0,len(poss) - 1)
            nextNode = poss[choice]

        #If ever we get to a point where the current node has no options
        #create an edge between it and the node it came from
        if len(poss) == 0:
               nextNode = prevNode
               
        #Add the edges and nodes to used so we avoid visiting them again
        maze[current[0]][current[1]].append(nextNode)
        maze[nextNode[0]][nextNode[1]].append(current)
        used.append(current)
        usedEdges.append((current, nextNode))
        
        #Make sure to avoid adding any nodes that have already been visited.
        for i in poss:
            if i in used:
                pass
            else:
                fringe.append((i,current))
                
    #Based on the algorithm we have to make a connection between
    #One of the bottom nodes with another manually or else a section
    #Will be cut off

    #Makes sure that every possible move is made from these nodes
    #To ensure that the maze is completely connected
    for i in range(math.floor(m/2) - 1, math.floor(m/2) + 1):
        current = (n-1, i)
        poss = edgeList[n-1][i]
        for j in range(len(poss)):
            nextNode = poss[j]
            if nextNode == current:
                pass
            else:
                maze[current[0]][current[1]].append(nextNode)
                maze[nextNode[0]][nextNode[1]].append(current)
                used.append(current)
                usedEdges.append((current, nextNode)) 
    printMazeTriangle(maze,n,m)

    
PrimMazeRectangle(7,7,(0,0))
print()
PrimMazeCircle(15)
print()
PrimMazeTriangle(15)

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
