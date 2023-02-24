
import turtle
from tkinter import *  
from tkinter import messagebox  

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
        self.speed(0)

class Player (turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(0.5, 0.5, 0.5)
        self.color ("green")
        self.penup()
        self.speed(0)
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
def display_maze (maze_configuration, n):
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -583 + ((((64-n)//2) + x) * 18)
            screen_y = 583 - ((((64-n)//2)+ y) * 18)
            #Check if it is an X (representing a wall)

            if character == "#":
                wall.goto(screen_x, screen_y)
                wall.stamp()
            if character == "S":
                player.goto(screen_x, screen_y)
                player.stamp()
            if character == "G":
                goal.goto(screen_x, screen_y)
                goal.stamp()
            


#update the grid after each action
def maze_optimalpath(maze_configuration, optimal_path, n):
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -583 + ((((64-n)//2) + x )* 18)
            screen_y = 583 - ((((64-n)//2)+y) * 18)

            if character == "X":
                wall.goto(screen_x, screen_y)
                wall.stamp()
            if (optimal_path is not None):
                if [y,x] in optimal_path:
                    player.goto(screen_x, screen_y)
                    player.stamp()


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
        count += 1
        initializeDisplay(displayMaze, size)
        

        if len(frontier) > 1:
            frontier.sort(key=lambda node: node.cost_with_heuristic)
    
        #since sorted, get the first node in the list
        current_node = frontier[0]

        updateDisplay(displayMaze,current_node, size)
        
        
        # Pop the current of frontier, add this to explored
        frontier.pop(0)
        explored.append(current_node)

        if current_node == goalNode:
            optimalPath = []
            while current_node is not None:
                optimalPath.append(current_node.coordinate)
                current_node = current_node.parent
            return optimalPath[::1]
            
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
    #initialize start and goal states
    for i in range(size):
        if 'S' in maze[i]:
            startNode = State([i, maze[i].index('S')], None)
        elif 'G' in maze[i]:
            goalNode = State([i, maze[i].index('G')], None)
            
    startNode.h = aStar(goalNode, startNode)
    startNode.cost_with_heuristic = startNode.h
    display_maze(maze, size)
    optimal_path = mazeSearch(startNode,goalNode,maze,size)
    if optimal_path is None:
        print("No path found.")
        messagebox.showwarning("Note","No path found") 
        turtle.exitonclick()
        
    else:    
        maze_optimalpath(maze, optimal_path, size)
    turtle.exitonclick()

    

if __name__ == '__main__':
    main()
    
    
