"""
This is to certify that this project is our own work, based on our personal efforts in studying and
applying the concepts learned. We have constructed the functions and their respective algorithms 
and corresponding code by ourselves. The program was run, tested, and debugged by our own efforts. 
We further certify that we have not copied in part or whole or otherwise plagiarized the work 
of other students and/or persons.

Daphne Janelyn Go
Enrique Rafael Lejano
Maria Monica Manlises
Krizchelle Danielle Wong

INSTRUCTIONS FOR RUNNING THE PROGRAM:
1. If your current version of Python is 3.10 and below, run this statement (brew install python-tk@3.<Version Number>) on the command prompt. 
Ex: brew install python-tk@3.10
2. To input the maze configuration, simply paste your maze configuration test case to maze.txt located in the folder. As an alternative, 
you can delete the said file and make your own maze.txt file with your chosen maze configuration. 
3. Once you run the program, an application box should appear. For better viewing, please maximize the application. 
4. Once the bot is able to reach its goal node, a simple mouse click in any black space in the application will terminate the program.
Terminating the program before it reaches the goal node or terminating the search requires clicking the exit button. 
5. As an alternative view, the maze is also displayed via the command prompt. 


"""
import turtle
from tkinter import messagebox 
import time
from warnings import warn
import math

window = turtle.Screen()
window.bgcolor("black")
window.title("Maze Bot")
window.screensize()
window.setup(width = 1.0, height = 1.0)
walls=[]

#Code for GUI
class Icon (turtle.Turtle):
    def __init__(self):
        """
         Initialize turtle with default parameters for the size of the maze walls.
        """
        turtle.Turtle.__init__(self) 
        self.shape ("square")
        self.shapesize(0.7, 0.7, 0.5)
        self.color ("white")
        self.penup()
        self.speed(0)

class Player (turtle.Turtle):
    def __init__(self):
        """
         Initialize turtle for player color, size and penup
        """
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.shapesize(0.3, 0.3, 0.5)
        self.color ("green")
        self.penup()
        self.speed(0)


class Path (turtle.Turtle):
    def __init__(self):
        """
         Initialize turtle with default parameters for the size of the path configuration outline
        """
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(0.3, 0.3, 0.5)
        self.color ("yellow")
        self.penup()
        self.speed(0)
        self.hideturtle()

class Goal (turtle.Turtle):
    def __init__(self):
        """
         Initialize turtle with default parameters for goal size and color
        """
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.shapesize(0.3, 0.3, 0.5)
        self.color ("red")
        self.penup()
        self.speed(0)
        self.hideturtle()

class optimalPath (turtle.Turtle):
    def __init__(self):
        """
         Initialize turtle with default parameters for the size of the path configuration outline
        """
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.shapesize(0.3, 0.3, 0.5)
        self.color ("yellow")
        self.penup()
        self.speed(0)
        self.hideturtle()

        

# create a grid for maze configuration 
def display_maze (maze_configuration, n):
    """
     Displays maze in n tiles. This is a function to be called from display_maze.
     
     @param maze_configuration - A 2D array of character values
     @param n - The number of tiles
    """
    # Find the maze configuration for the given number of points.
    for y in range (n):
        # Find the maze configuration for the given x y coordinates.
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -383 + ((((64-n)//2) + x) * 12)
            screen_y = 383 - ((((64-n)//2)+ y) * 12)
            
            # If character is a # or a #, stamp the wall icon.
            if character == "#":
                wall.goto(screen_x, screen_y)
                walls.append((screen_x, screen_y))
                wall.stamp()
            # If the character is S, stamp the player icon.
            if character == "S":
                player.goto(screen_x, screen_y)
            # If the character is S, stamp the goal icon.
            if character == "G":
                goal.goto(screen_x, screen_y)
                goal.stamp()
            # Skips if it is a . or o character.
            if (character == '.' or character == '*' or character == 'o'):
                continue
        
#update the grid after each action
def move_player (maze_configuration, n):
    """
     Move the player to the coordinates of the maze. This is used to make the game easier and more easily to play
     
     @param maze_configuration - The configuration of the maze
     @param n - The number of characters to move in the maz
    """
    path.clear()
    # Find the maze configuration for the given number of points
    for y in range (n):
        # Find the xy coordinates of the character.
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -383 + ((((64-n)//2) + x) * 12)
            screen_y = 383 - ((((64-n)//2)+ y) * 12)

            #Check where o is
            # Set the screen position on the player
            if character == 'o':      
                player.setx(screen_x)
                player.sety (screen_y)
            # Check where * is
            # Set the screen position on the path configuration
            if character == '*':
                path.goto(screen_x, screen_y)
                path.stamp()
                                     
def maze_optimalpath(maze_configuration, optimal_path, n):
    """
     This function takes a maze configuration and an optimal path. It moves the wall to the coordinates of the character that leads to the maze and checks if there is an optimal path.
     
     @param maze_configuration - The maze configuration as a 2D array
     @param optimal_path - The list of possible optimal path
     @param n - The number of points to move in the m
    """
    
    for y in range (n):
        # Find the screen x y coordinates of the maze configuration.
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -383 + ((((64-n)//2) + x )* 12)
            screen_y = 383 - ((((64-n)//2)+y) * 12)

            if character == "X":
                wall.goto(screen_x, screen_y)
                wall.stamp()
        
            if (optimal_path is not None):
                # If y x is in optimal path.
                if [y,x] in optimal_path:
                    path.goto(screen_x, screen_y)
                    path.stamp()


wall = Icon()
player = Player()
path = Path()
goal = Goal()
optimalpath = optimalPath()


#Code for Main Logic and Search Algorithm
class State():
    def __init__(self, coordinate = None, parent = None):
        """
         Initialize the class with a coordinate and a parent. This is used to set the cost_with_heuristic to - 1 and the g and h attributes to 0
         
         @param coordinate - The coordinate to use for the cost
         @param parent - The parent of the coordinate to use for the
        """
        self.coordinate = coordinate
        self.g = 0
        self.h = 0
        self.cost_with_heuristic = -1
        self.parent = parent
    
    def __eq__(self, other):
        """
         @return True if the coordinates are equal False otherwise.
        """
        return self.coordinate == other.coordinate

def heuristic(goal, currentNode):
    """
     Calculates the aStar between two points. It is assumed that the points are in the same coordinate system
     
     @param goal - The goal state of the maze
     @param currentNode - The current point to be considered 
     
     @return The euclidean distance
    """
    return math.sqrt((goal.coordinate[0] - currentNode.coordinate[0]) ** 2 + (goal.coordinate[1] - currentNode.coordinate[1]) ** 2)

def initializeDisplay(maze, size):
    """
     Replaces spaces in maze with spaces. This is used to make the display easier to read.
     
     @param maze - The maze to be displayed
     @param size - The size of the maze
    """
    for i in range (size):
        for j in range (size):
            if (maze[i][j] == '.' or maze[i][j] == '*' or maze[i][j] == 'o'):
                maze[i][j] = ' '
            elif (maze[i][j] == '#'):
                maze[i][j] = 'X'
            elif(maze[i][j] == 'S'):
                maze[i][j] = 'o'
        
def updateDisplay(displayMaze, current_node, size):
    """
     Updates the display maze. This is a helper function to make it easier to use in an interactive program
     
     @param displayMaze - A 2D array of display mazes
     @param current_node - The node to display 
     @param size - The size of the maze
    """
    x = current_node.coordinate[0]
    y = current_node.coordinate[1]

    displayMaze[x][y] = 'o'

    # Find the coordinate of the current node.
    while current_node.parent is not None:
        x = current_node.parent.coordinate[0]
        y = current_node.parent.coordinate[1]

        displayMaze[x][y] = '*'

        current_node = current_node.parent

    # Prints the maze in an n x n matrix
    for i in range (size):
        # Print the maze in the current size
        for j in range (size):
            print (displayMaze[i][j], end = ' ')
        print ("\n")


def mazeSearch(startNode, goalNode, maze, size):
    """
     Search the maze for a goal. This is a function that uses heuristics to determine the frontier 
     and explores the nodes in the maze until there are no more nodes to explore
     
     @param startNode - The node that we start from
     @param goalNode - The node that we want to go to
     @param maze - The maze to search through
     @param size - The size of the player in maze
     
     @return A list of nodes that have been explored from the maze and the number of times it
    """
    # Initialize frontier and explored list
    frontier = []
    explored = []
    displayMaze = maze.copy()
    
    frontier.append(startNode)
    count = 0
    
    # This function is used to find the optimal path to the frontier.
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
        
        move_player(displayMaze, size)

        
        w = turtle.Turtle()
        w.color ("white")
        w.penup()
        w.goto (-490, 350)
        w.pendown()
        style = ('Courier', 10, 'normal')
        w.write("States Explored = " + str(count), font = style, align ='center')
        start = time.time()
        # This function is used to delay the counter prompt for easier visibility.
        while time.time () - start < 0.3:
            pass
        w.undo()
        w.hideturtle()


        # Returns the optimal path of the goal node.
        if current_node == goalNode:
            optimalPath = []
            # appends coordinate to optimalPath.
            while current_node is not None:
                optimalPath.append(current_node.coordinate)
                current_node = current_node.parent
            return optimalPath
            
        # check children
        x = current_node.coordinate[0]
        y = current_node.coordinate[1]
        
        children = []
        # Add a state to the children list
        if x + 1 < size:
            if maze[x+1][y] == ' ' or maze[x+1][y] == 'G':
                new_state = State([x+1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = heuristic(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
        if x-1 > -1:
            if maze[x-1][y] == ' ' or maze[x-1][y] == 'G':
                new_state = State([x-1, y], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = heuristic(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)

        if y + 1 < size:
            if maze[x][y+1] == ' ' or maze[x][y+1] == 'G':
                new_state = State([x, y + 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = heuristic(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
            
        if y - 1 > -1:
            if maze[x][y-1] == ' ' or maze[x][y-1] == 'G':
                new_state = State([x, y - 1], current_node)
                if new_state not in explored:
                    new_state.g = current_node.g + 1
                    new_state.h = heuristic(goalNode,new_state)
                    new_state.cost_with_heuristic = new_state.g + new_state.h
                    children.append(new_state)
        if (len(children) > 0):  
            # Add the node to frontier.
            for node in children:
                # Child is already in the open list
                if len([open_node for open_node in frontier if node.coordinate == open_node.coordinate and node.g > open_node.g]) > 0:
                    continue
                frontier.append (node)
        print ("\n")
        
    print("No path found.")
    return None

        

def main ():
    """
     Main function for maze search. Reads the maze. txt file and uses astar algorithm to find the optimal path
    """
    i = 0
    optimal_path = []
    

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
            
    startNode.h = heuristic(goalNode, startNode)
    startNode.cost_with_heuristic = startNode.h
    display_maze(maze, size)
    optimal_path = mazeSearch(startNode,goalNode,maze,size)
    if optimal_path is not None:
        maze_optimalpath(maze, optimal_path, size)
        turtle.exitonclick()
    else:
        messagebox.showwarning("Note","No path found") 
        turtle.exitonclick()

    

if __name__ == '__main__':
    main()
    
    
