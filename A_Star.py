class Node():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0 # g score + h score
        self.g = 0 # distance from the start node to the current node 
        self.h = 0 # approximate distance from the current node to the end node
        self.neighbours = []
        self.previous = None
        self.wall = None

    def isSnake(self, snake):
        # check every part of the snake if this node is a part of the snake set this node as a obstacle
        for rect in snake.body:
            if rect.x//snake.size == self.j and rect.y//snake.size == self.i:
                self.wall = True
                return
        
        self.wall = False



    def addNeighbours(self, grid, rows, columns):
        # Gives every node neighbours 
        i = self.i
        j = self.j

        if i < columns-1: # down 
            self.neighbours.append(grid[i+1][j])
        if i > 0: # up
            self.neighbours.append(grid[i-1][j])
        if j < rows - 1: # right
            self.neighbours.append(grid[i][j+1])
        if j > 0: # left
            self.neighbours.append(grid[i][j-1])

    def heuristic(self, a, b):
        # Approximates the distance from the current node to the end node
        d = abs(a.i-b.i) + abs(a.j-b.j)
        return d


def A_star(start, end):
    openSet = [start]
    closedSet = []

    while len(openSet) != 0:
        # set current to the node in with the lowest f score in the openSet
        winner = 0
        for i in range(len(openSet)):
            if (openSet[i].f < openSet[winner].f):
                winner = i

        current = openSet[winner]

        # if current is the end trace back the path and return it
        if current == end:
            # Find the path
            path = []
            temp = current
            path.append(current)
            while temp.previous:
                path.append(temp.previous)
                temp = temp.previous

            return path

        # if it is not the end append this node to closedSet and remove it from openSet as it is evaluated
        closedSet.append(current)
        openSet.remove(current)

        # choose the next node to evaluated as the neighbour of the current node with the lowest g score and its not a obstacle
        neighbours = current.neighbours
        for neighbour in neighbours:
            if neighbour not in closedSet and not neighbour.wall:
                tempG = current.g + 1
                if neighbour in openSet:
                    if tempG < neighbour.g:
                        neighbour.g = tempG
                else:
                    neighbour.g = tempG
                    openSet.append(neighbour)

                neighbour.h = neighbour.heuristic(neighbour, end)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.previous = current

    print('No solution')
    exit(0)
