import sys

goalState = [[1, 2, 3],
             [8, 0, 4],
             [7, 6, 5]
             ]

# locates the index of a tile on a given board
def locateTile(board, tile):
    for index, row in enumerate(board):
        if tile in row:
            return [index, row.index(tile)]

# calculates manhattan distance heuristic
def manhattanDistance(start, goal, tile):
    # find indices of tile in both start and goal
    startLoc = locateTile(start, tile)
    goalLoc = locateTile(goal, tile)

    # subtract the indices to calculate the distance and return it
    return abs(startLoc[0] - goalLoc[0]) + abs(startLoc[1] - goalLoc[1])

def getAdjacentTiles(start, tile):
    baseTileLoc = locateTile(start, tile)
    results = []

    adjTiles = [[baseTileLoc[0] + 1, baseTileLoc[1]],
                [baseTileLoc[0], baseTileLoc[1] + 1],
                [baseTileLoc[0] - 1, baseTileLoc[1]],
                [baseTileLoc[0], baseTileLoc[1] - 1]
                ]

    for adjTile in adjTiles:
        if all(i > 0 and i < 3 for i in adjTile):
            results.append(start[adjTile[0]][adjTile[1]])

    return results


def moveTile(start, tile):
    emptyTile = locateTile(start, 0)
    tileToMove = locateTile(start, tile)

    newBoard = start
    newBoard[emptyTile[0]][emptyTile[1]] = tile
    newBoard[tileToMove[0]][tileToMove[1]] = 0
    return newBoard

# read input state from file and save it as a 2D (3x3) list
f = open("startState", 'r')
startState = []
for line in f.readlines():
    startState.append(list(map(int, line.strip())))

#print(goalState[0], goalState[1], goalState[2])
print('', startState[0], '\n', startState[1], '\n', startState[2], '\n')
tile = 1
# f = h + g

pathCost = 0
prevMove = 0
bestMove = 0
while startState != goalState:
    # find all tiles adjacent to the empty tile
    availableMoves = getAdjacentTiles(startState, 0)

    # disallow moving the same tile twice in a row (back and forth endlessly)
    if prevMove in availableMoves:
        availableMoves.remove(prevMove)

    # find the lowest cost tile to move which is adjacent to the empty tile
    lowestCost = sys.maxsize
    for tile in availableMoves:
        h = manhattanDistance(startState, goalState, tile)
        # f = g(tile) + h(manhatdist)
        if tile + h < lowestCost:
            lowestCost = tile + h
            bestMove = tile
    # execute the move
    startState = moveTile(startState, bestMove)

    # add the move to the overall cost of the path
    pathCost += lowestCost
    prevMove = bestMove
    bestMove = 0
    print('', startState[0], '\n', startState[1], '\n', startState[2], '\n', 'cost:', lowestCost, 'total Cost:', pathCost)

print(pathCost)

