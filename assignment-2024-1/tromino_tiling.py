import sys

def calculateCenter(startX, endX, startY, endY):
        centerX = int((startX + endX) / 2)
        centerY = int((startY + endY) / 2)
        return centerX, centerY

def fill(n, grid, startX, endX, startY, endY, missingX, missingY):

    #GET CENTER OF THE CURRENT RECTANGLE AND SET THE MIDDLE COORDINATES
    #ul= Upper Left, ur= Upper Right, ll= Lower Left, lr= Lower Right

    cX, cY = calculateCenter(startX, endX, startY, endY)

    ulX, ulY = cX, cY
    urX, urY = cX+1, cY
    llX, llY = cX, cY+1
    lrX, lrY = cX+1, cY+1

    #CHECK IF THE MISSING TILE IS ON THE LEFT (OR OTHERWISE THE RIGHT) OF THE GRID
    #CHECK IF THE MISSING TILE IS ON THE UPPER (OR OTHERWISE THE LOWER) OF THE GRID

    if missingX <= cX:  #LEFT
        if missingY <= cY: #LEFT AND UPPER BOUND
            makeTromino(grid, cX, cY+1, cX+1, cY+1, cX+1, cY, n)
            ulX, ulY = missingX, missingY
        else: #LEFT AND LOWER BOUND
            makeTromino(grid, cX, cY, cX+1, cY, cX+1, cY+1, n)
            llX, llY = missingX, missingY
    else: #RIGHT
        if missingY <= cY: #RIGHT AND UPPER BOUND
            makeTromino(grid, cX, cY, cX, cY+1, cX+1, cY+1, n)            
            urX, urY = missingX, missingY
        else: #RIGHT AND LOWER BOUND
            makeTromino(grid, cX, cY, cX+1, cY, cX, cY+1, n)
            lrX, lrY = missingX, missingY

    if n==1:
        return
    else:
        fill(n-1, grid, startX, cX, startY, cY, ulX, ulY) #RECURSION FOR UL
        fill(n-1, grid, cX+1, endX, startY, cY, urX, urY) #RECURSION FOR UR
        fill(n-1, grid, startX, cX, cY+1, endY, llX, llY) #RECURSION FOR LL
        fill(n-1, grid, cX+1, endX, cY+1, endY, lrX, lrY) #RECURSION FOR LR
    
def placeTile(grid, x, y, n):
    grid[x][y] = n        
    
#PLACES TILES AROUND THE MISSING TILE - THE HOLE
def makeTromino(grid, x1, y1, x2, y2, x3, y3, n):
    placeTile(grid, x1, y1, n)
    placeTile(grid, x2, y2, n)
    placeTile(grid, x3, y3, n)

def showGrid(grid):
    for j in range(len(grid)):
        for i in range(len(grid)):
            print(grid[i][j], end=" ")
        print()
    print()            

def tileGrid(n): 
    size = 2**n
    if n==1:
        missingX = 1
        missingY = 0
    else: 
        missingX = 3
        missingY = 3    

    grid = [['X' if i == missingY and j == missingX else '0' for i in range(size)] for j in range(size)]
    fill(n, grid, 0, size-1, 0, size-1, missingX, missingY)
    showGrid(grid)

n = int(sys.argv[1])
tileGrid(n)
