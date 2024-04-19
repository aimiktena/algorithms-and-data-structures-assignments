import sys

def calculateCenter(startX, endX, startY, endY):
    centerX = int((startX + endX) / 2)
    centerY = int((startY + endY) / 2)
    return centerX, centerY
 
# DEFINE THE 2 FOLLOWING FUNCTIONS IN ORDER TO CONVERT THE TILING PROBLEM TO A GRAPH COLORING PROBLEM (FOR THE COLORING OF THE TROMINOS)
def are_adjacent(position1, position2):
    x1, y1 = position1
    x2, y2 = position2    
    return abs(x1 - x2) <=1 and abs(y1 - y2) <=1

def assign_neighbours(tromino_positions):
    num_trominos = len(tromino_positions)
    # INITIALIZE LIST OF LISTS FOR STORING THE NEIGHBOURS
    neighbours = [[] for _ in range(num_trominos)]  

    for i in range(num_trominos):
        for j in range(i + 1, num_trominos):  
            is_neighbour = False
            for position1 in tromino_positions[i]:
                for position2 in tromino_positions[j]:
                    if are_adjacent(position1, position2):
                        is_neighbour = True
                        break 
                if is_neighbour:
                    break  
            if is_neighbour:
                neighbours[i].append(j)
                neighbours[j].append(i)  

    return neighbours

def fill(n, grid, startX, endX, startY, endY, tromino_nums, tromino_positions, missingX, missingY):
    tromino_index = tromino_nums.pop(0)  # INDEX OF CURRENT TROMINO THAT WILL BE CREATED
    tromino_nums.append(tromino_index)  # MOVES THE INDEX OF THIS TROMINO TO THE END SO THAT IT CAN NOT BE REUSED

    # GET CENTER OF THE CURRENT RECTANGLE AND SET THE MIDDLE COORDINATES
    # ul= Upper Left, ur= Upper Right, ll= Lower Left, lr= Lower Right    
    cX, cY = calculateCenter(startX, endX, startY, endY)

    ulX, ulY = cX, cY
    urX, urY = cX+1, cY
    llX, llY = cX, cY+1
    lrX, lrY = cX+1, cY+1

    # CHECK IF THE MISSING TILE IS ON THE LEFT (OR OTHERWISE THE RIGHT) OF THE GRID
    # CHECK IF THE MISSING TILE IS ON THE UPPER (OR OTHERWISE THE LOWER) OF THE GRID

    if missingX <= cX:  # LEFT
        if missingY <= cY: # LEFT AND UPPER BOUND
            makeTromino(grid, cX, cY+1, cX+1, cY+1, cX+1, cY, tromino_index)
            tromino_positions.append([(cX, cY+1), (cX+1, cY+1), (cX+1, cY)])
            ulX, ulY = missingX, missingY
        else: # LEFT AND LOWER BOUND
            makeTromino(grid, cX, cY, cX+1, cY, cX+1, cY+1, tromino_index)
            tromino_positions.append([(cX, cY), (cX+1, cY), (cX+1, cY+1)])
            llX, llY = missingX, missingY
    else: # RIGHT
        if missingY <= cY: # RIGHT AND UPPER BOUND
            makeTromino(grid, cX, cY, cX, cY+1, cX+1, cY+1, tromino_index)  
            tromino_positions.append([(cX, cY), (cX, cY+1), (cX+1, cY+1)])
            urX, urY = missingX, missingY
        else: # RIGHT AND LOWER BOUND
            makeTromino(grid, cX, cY, cX+1, cY, cX, cY+1, tromino_index)
            tromino_positions.append([(cX, cY), (cX+1, cY), (cX, cY+1)])
            lrX, lrY = missingX, missingY

    if n == 1:
        return 
    else:
        fill(n-1, grid, startX, cX, startY, cY, tromino_nums, tromino_positions, ulX, ulY) # RECURSION FOR UL
        fill(n-1, grid, cX+1, endX, startY, cY, tromino_nums, tromino_positions, urX, urY) # RECURSION FOR UR
        fill(n-1, grid, startX, cX, cY+1, endY, tromino_nums, tromino_positions, llX, llY) # RECURSION FOR LL
        fill(n-1, grid, cX+1, endX, cY+1, endY, tromino_nums, tromino_positions, lrX, lrY) # RECURSION FOR LR

def placeTile(grid, x, y, n):
    grid[x][y] = n        

# PLACES TILES AROUND THE MISSING TILE - THE HOLE
def makeTromino(grid, x1, y1, x2, y2, x3, y3, n):
    placeTile(grid, x1, y1, n)
    placeTile(grid, x2, y2, n)
    placeTile(grid, x3, y3, n)

def showGrid(grid):
    for j in range(len(grid)):
        for i in range(len(grid)):
            print(grid[i][j], end=" ")
        print()            

def tileGrid(n): 
    size = 2**n
    if n == 1:
        missingX = 1
        missingY = 0
    else: 
        missingX = 3
        missingY = 3   

    # INITILIAZE GRID AND PLACE THE MISSING TILE / HOLE WITH AN 'X'
    grid = [['X' if i == missingY and j == missingX else '0' for i in range(size)] for j in range(size)] 
    # INITIALIZE THE LIST OF INDEXES FOR EACH TROMINO SO THAT IT CAN START COUNTING FROM 0
    tromino_nums = list(range(size * size))
    # INITILIAZE LIST TO STORE THE POSITIONS OF EACH TROMINO
    tromino_positions = []  

    fill(n, grid, 0, size-1, 0, size-1, tromino_nums, tromino_positions, missingX, missingY)
    showGrid(grid)
    
n = int(sys.argv[1])
tileGrid(n)
