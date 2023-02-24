
import turtle

window = turtle.Screen()
window.bgcolor("black")
window.title("Maze Bot")
window.setup(740,740)


#Code for GUI
class Icon (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self) 
        self.shape ("square")
        self.shapesize(1.0, 1.0, 2.0)
        self.color ("white")
        self.penup()
        self.speedup= 0

class Player (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(0.5, 0.5, 0.5)
        self.color ("green")
        self.penup()
        self.speed(0)
        def hide(self):
            self.hideturtle()

class Path (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(0.5, 0.5, 0.5)
        self.color ("blue")
        self.penup()
        self.speed(0)
        self.hideturtle()

class Goal (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.shapesize(0.5, 0.5, 0.5)
        self.color ("red")
        self.penup()
        self.speed(0)
        self.hideturtle()

class optimalPath (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.shapesize(0.5, 0.5, 0.5)
        self.color ("yellow")
        self.penup()
        self.speed(0)
        self.hideturtle()

# create a grid for maze configuration 
def setup_maze (maze_configuration, n):
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -529 + ((((64-n)//2) + x) * 18)
            screen_y = 529 - ((((64-n)//2)+ y) * 18)
            #Check if it is an X (representing a wall)
            if character == "X":
                wall.goto(screen_x, screen_y)
                wall.stamp()
            if character == "o":
                player.goto(screen_x, screen_y)
                player.stamp()
            if character == "G":
                goal.goto(screen_x, screen_y)
                goal.showturtle()
                goal.stamp()


#update the grid after each action
def update_maze(maze_configuration, n):
    goal.hideturtle()
    path.hideturtle()
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -523 + ((((64-n)//2) + x )* 18)
            screen_y = 523 - ((((64-n)//2)+y) * 18)
            #Check if it is an X (representing a wall)
            if character == "*":
                path.goto(screen_x, screen_y)
                path.showturtle()
                path.stamp()

            if character == "o":
                player.goto(screen_x, screen_y)
                player.stamp()
def show_path (maze_configuration, n):
    goal.hideturtle()
    path.hideturtle()
    optimalpath.hideturtle()
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -523 + ((((64-n)//2) + x )* 18)
            screen_y = 523 - ((((64-n)//2)+y) * 18)
            #Check if it is an X (representing a wall)
            if character == "@":
                optimalpath.goto(screen_x, screen_y)
                optimalpath.showturtle()
                optimalpath.stamp()

wall = Icon()
player = Player()
path = Path()
goal = Goal()
optimalpath = optimalPath()


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
    return ((currentNode.coordinate[0] - goal.coordinate[0]) ** 2) + ((currentNode.coordinate[1] - goal.coordinate[1]) ** 2)

def initializeDisplay(maze, size):
    for i in range (size):
        for j in range (size):
            if (maze[i][j] == '.'):
                maze[i][j] = ' '
            elif (maze[i][j] == '#'):
                maze[i][j] = 'X'
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

def highlight_path (optimal_path, display_maze, size):
    for i in range (size):
        for j in range (size):
            if (i,j) in optimal_path:
                print("True")
                display_maze[i][j]= '@'
    for i in range (size):
        for j in range (size):
            print (display_maze[i][j], end = ' ')
        print ("\n")


def mazeSearch(startNode, goalNode, maze, size, displayMaze):
    # Initialize frontier and explored list
    frontier = []
    explored = []
    
    frontier.append(startNode)
    count = 0
    
    while len(frontier) > 0:

        '''if len(frontier) > 1:
            frontier.sort(key=lambda node: node.cost_with_heuristic)
        for state in explored:
            print(state.coordinate)'''
        
        #since sorted, get the first node in the list
        current_node = frontier[0]
        current_index = 0

        for index, node in enumerate(frontier):
            if node.cost_with_heuristic < current_node.cost_with_heuristic:
                current_node = node
                current_index = index
        
        if current_node != startNode:
            updateDisplay(displayMaze,current_node, size)
            update_maze(displayMaze, size)
        
        # Pop the current of frontier, add this to explored
        frontier.pop(current_index)
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

        for node in children:
            for open_node in frontier:
                if node == open_node and node.g > open_node.g:
                    continue
            frontier.append(node)
        print ("\n")
        

def main ():
    i = 0
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
    displayMaze = maze.copy()
    initializeDisplay(displayMaze, size)
    setup_maze (displayMaze, size)
    optimal_path = []
    optimal_path = mazeSearch(startNode,goalNode,maze,size,displayMaze)
    print(optimal_path)

    '''
    print ("\n")
    highlight_path(optimal_path, displayMaze, size)
    show_path(displayMaze, size)
    turtle.exitonclick()
    '''
    

if __name__ == '__main__':
    main()
    
    
