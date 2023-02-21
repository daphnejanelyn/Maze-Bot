import math

class State():
    def __init__(self, coordinate = None, parent = None):
        self.coordinate = coordinate
        self.g = 0
        self.h = 0
        self.cost_with_heuristic = -1
        self.parent = parent
    
    def __eq__(self, other):
        return self.coordinate == other.coordinate

def aStar(goal, currentNode):
    return math.sqrt((goal.coordinate[0] - currentNode.coordinate[0]) ** 2 + (goal.coordinate[1] - currentNode.coordinate[1]) ** 2)

def initializeDisplay(maze, size):
    for i in range (size):
        for j in range (size):
            if (maze[i][j] == '.'):
                maze[i][j] = 'x'
            elif (maze[i][j] == '#'):
                maze[i][j] = 'w'
            elif(maze[i][j] == 'S'):
                maze[i][j] = 'o'
    for i in range (size):
        for j in range (size):
            print (maze[i][j], end = ' ')
        print ("\n")
        
def updateDisplay(current_maze, current_node, size):
    x = current_node.coordinate[0]
    y = current_node.coordinate[1]

    current_maze[x][y] = 'o'

    x = current_node.parent.coordinate[0]
    y = current_node.parent.coordinate[1]

    current_maze[x][y] = '*'

    for i in range (size):
        for j in range (size):
            print (current_maze[i][j], end = ' ')
        print ("\n")


def mazeSearch(startNode, goalNode, maze, size, displayMaze):
    # Initialize frontier and explored list
    frontier = []
    explored = []
    
    frontier.append(startNode)
    
    
    while len(frontier) > 0:

        if len(frontier) > 1:
            frontier.sort(key=lambda node: node.cost_with_heuristic)
        
        #since sorted, get the first node in the list
        current_node = frontier[0]
        
        if current_node != startNode:
            updateDisplay(displayMaze,current_node, size)
        
        # Pop the current of frontier, add this to explored
        frontier.pop(0)
        explored.append(current_node)

        if current_node == goalNode:
            optimalPath = []
            while current_node is not None:
                optimalPath.append(current_node.coordinate)
                current_node = current_node.parent
            return optimalPath
            
        # check children
        x = current_node.coordinate[0]
        y = current_node.coordinate[1]
        
        children = []
        if x + 1 < size:
            if maze[x+1][y] == 'x' or maze[x+1][y] == 'G':
                new_state = State([x+1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,current_node)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)

        if x-1 > -1:
            if maze[x-1][y] == 'x' or maze[x-1][y] == 'G':
                new_state = State([x-1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,current_node)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)

        if y + 1 < size:
            if maze[x][y+1] == 'x' or maze[x][y+1] == 'G':
                new_state = State([x, y + 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,current_node)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
            
        if y - 1 > -1:
            if maze[x][y-1] == 'x' or maze[x][y-1] == 'G':
                new_state = State([x, y - 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,current_node)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
        for node in children:
            for open_node in frontier:
                if node == open_node and node.g > open_node.g:
                    continue
        frontier.append(node)
        print ("\n")
        

def main ():
    i = 0

    with open("maze.txt") as f:
        size = int (f.readline())
        maze = [[]*size for i in range(size)] #initalize as a n by n matrix
        for line in f:
            line = line.rstrip()
            for letter in line:
                maze[i].append(letter)
            i += 1
    f.close()
    
    #initialize st)art and goal states
    for i in range(size):
        if 'S' in maze[i]:
            startNode = State([i, maze[i].index('S')], None)
        elif 'G' in maze[i]:
            goalNode = State([i, maze[i].index('G')], None)
            
    startNode.h = aStar(goalNode, startNode)
    startNode.cost_with_heuristic = startNode.h
    displayMaze = maze.copy()
    initializeDisplay(displayMaze, size)
    mazeSearch(startNode,goalNode,maze,size,displayMaze)

if __name__ == '__main__':
    main()
    
    