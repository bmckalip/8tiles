import sys
import copy

class board:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.cost = 0
        self.path = []

    # locates the index of a tile on a given board
    @staticmethod
    def locateTile(board, tile):
        for index, row in enumerate(board):
            if tile in row:
                return [index, row.index(tile)]

    # calculates manhattan distance heuristic
    def manhattanDistance(self, tile):
        # find indices of tile in both start and goal
        startLoc = self.locateTile(self.start, tile)
        goalLoc = self.locateTile(self.goal, tile)

        # subtract the indices to calculate the distance and return it
        return abs(startLoc[0] - goalLoc[0]) + abs(startLoc[1] - goalLoc[1])

    # returns all adjacent tiles to the specified tile
    def getAdjacentTiles(self, tile):
        baseTileLoc = self.locateTile(self.start, tile)
        results = []

        adjTiles = [[baseTileLoc[0] + 1, baseTileLoc[1]],
                    [baseTileLoc[0], baseTileLoc[1] + 1],
                    [baseTileLoc[0] - 1, baseTileLoc[1]],
                    [baseTileLoc[0], baseTileLoc[1] - 1]
                    ]

        # bound checking
        for adjTile in adjTiles:
            if all(i >= 0 and i <= 2 for i in adjTile):
                results.append(start[adjTile[0]][adjTile[1]])

        return results

    # returns the optimal move based on the lowest overall stochasticity of a proposed move
    def getBestMove(self, moves):
        bestMove = None
        bestSum = sys.maxsize
        for move in moves:
            sum = 0
            testBoard = copy.deepcopy(self)
            testBoard.moveTile(move)
            for tile in range(1, 9):
                sum += testBoard.manhattanDistance(tile)

            if sum < bestSum:
                bestSum = sum
                bestMove = move

        self.cost += bestMove
        return bestMove

    # swaps the positions of the specified tile and the empty tile
    def moveTile(self, tile):
        emptyTile = self.locateTile(self.start, 0)
        tileToMove = self.locateTile(self.start, tile)

        self.start[emptyTile[0]][emptyTile[1]] = tile
        self.start[tileToMove[0]][tileToMove[1]] = 0
        self.path.append(tile)


# read input state from file and save it as a 2D (3x3) list, create the goal state
start = []
goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

f = open("startState", 'r')
for line in f.readlines():
    start.append(list(map(int, line.strip())))

print('', start[0], '\n', start[1], '\n', start[2])

currentState = board(start, goal)
prevMove = 0
bestMove = 0

# main algorithm loop
while currentState.start != goal:
    # find all tiles adjacent to the empty tile
    moves = currentState.getAdjacentTiles(0)

    # disallow moving the same tile twice in a row (back and forth endlessly)
    while True:
        bestMove = currentState.getBestMove(moves)
        if bestMove != prevMove:
            prevMove = bestMove
            break
        else:
            moves.remove(bestMove)

    # execute the move. uncomment print() statement to print the board after every step
    currentState.moveTile(bestMove)
    # print('\n', currentState.start[0], '\n', currentState.start[1], '\n', currentState.start[2])

# print Path information
print("\n Path: " + str(currentState.path),
      "\n Path Cost: " + str(currentState.cost)
      )


