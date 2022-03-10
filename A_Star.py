class Node():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = None
        self.wall = None

    def isSnake(self, snake):
        for rect in snake.body:
            if rect.x//snake.size == self.j and rect.y//snake.size == self.i:
                self.wall = True
                return
        self.wall = False



    def addNeighbours(self, grid, rows, columns):
        i = self.i
        j = self.j

        if i < columns-1:
            self.neighbours.append(grid[i+1][j])
        if i > 0:
            self.neighbours.append(grid[i-1][j])
        if j < rows - 1:
            self.neighbours.append(grid[i][j+1])
        if j > 0:
            self.neighbours.append(grid[i][j-1])

    def heuristic(self, a, b):
        d = abs(a.i-b.i) + abs(a.j-b.j)
        return d

    # def __str__(self):
    #     return f'i:{self.i}, j:{self.j}, is a snake:{self.isSnake}'


def A_star(start, end):
    openSet = [start]
    closedSet = []

    while len(openSet) != 0:
        winner = 0
        for i in range(len(openSet)):
            if (openSet[i].f < openSet[winner].f):
                winner = i

        current = openSet[winner]

        if current == end:
            # Find the path
            path = []
            temp = current
            path.append(current)
            while temp.previous:
                path.append(temp.previous)
                temp = temp.previous


            return path

        closedSet.append(current)
        openSet.remove(current)

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
