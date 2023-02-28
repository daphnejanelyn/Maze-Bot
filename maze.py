#Code for Main Logic and Search Algorithm
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
    return ((goal.coordinate[0] - currentNode.coordinate[0]) ** 2) + ((goal.coordinate[1] - currentNode.coordinate[1]) ** 2)

def initializeDisplay(maze, size):
    for i in range (size):
        for j in range (size):
            if (maze[i][j] == '.' or maze[i][j] == '*' or maze[i][j] == 'o'):
                maze[i][j] = ' '
            elif (maze[i][j] == '#'):
                maze[i][j] = 'X'
            elif(maze[i][j] == 'S'):
                maze[i][j] = 'o'
        
def updateDisplay(displayMaze, current_node, size):
    x = current_node.coordinate[0]
    y = current_node.coordinate[1]

    displayMaze[x][y] = 'o'

    while current_node.parent is not None:
        x = current_node.parent.coordinate[0]
        y = current_node.parent.coordinate[1]

        displayMaze[x][y] = '*'

        current_node = current_node.parent

    for i in range (size):
        for j in range (size):
            print (displayMaze[i][j], end = ' ')
        print ("\n")


def mazeSearch(startNode, goalNode, maze, size):
    # Initialize frontier and explored list
    frontier = []
    explored = []
    displayMaze = maze.copy()
    
    frontier.append(startNode)
    count = 0
    
    while len(frontier) > 0:
        print (len(frontier))
        count += 1
        initializeDisplay(displayMaze, size)

        frontier.sort(key=lambda node: node.cost_with_heuristic)
    
        #since sorted, get the first node in the list
        current_node = frontier[0]

        # Pop the current of frontier, add this to explored
        updateDisplay(displayMaze,current_node, size)
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
            if maze[x+1][y] == ' ' or maze[x+1][y] == 'G':
                new_state = State([x+1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)

        if x-1 > -1:
            if maze[x-1][y] == ' ' or maze[x-1][y] == 'G':
                new_state = State([x-1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)

        if y + 1 < size:
            if maze[x][y+1] == ' ' or maze[x][y+1] == 'G':
                new_state = State([x, y + 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
            
        if y - 1 > -1:
            if maze[x][y-1] == ' ' or maze[x][y-1] == 'G':
                new_state = State([x, y - 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = aStar(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
        if (len(children) > 0):  
            for node in children:
                # Child is already in the open list
                if len([open_node for open_node in frontier if node.coordinate == open_node.coordinate and node.g > open_node.g]) > 0:
                    continue
                frontier.append (node)
        print ("\n")
        
    print("No path found.")
    return None

        

def main ():
    i = 0
    optimal_path = []
    # Create class instances

    with open("maze.txt") as f:
        size = int (f.readline())
        maze = [[]*size for i in range(size)] #initalize as a n by n matrix
        for line in f:
            line = line.rstrip()
            for letter in line:
                maze[i].append(letter)
            i += 1
    f.close()
    
    #initialize start and goal states
    for i in range(size):
        if 'S' in maze[i]:
            startNode = State([i, maze[i].index('S')], None)
        elif 'G' in maze[i]:
            goalNode = State([i, maze[i].index('G')], None)
            
    startNode.h = aStar(goalNode, startNode)
    startNode.cost_with_heuristic = startNode.h

    optimal_path = mazeSearch(startNode,goalNode,maze,size)



    

if __name__ == '__main__':
    main()
    
    
