import turtle

window = turtle.Screen()
window.bgcolor("black")
window.title("Maze Bot")
window.setup(740,740)

'''Register shapes
turtle.register_shape("sea_turtle.png")
turtle.register_shape("red-flag.png")
'''


#Tentative setup, not sure if this is applicable
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
        self.color ("yellow")
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

# create a grid for maze configuration 
def setup_maze (maze_configuration, n):
    for y in range (n):
        for x in range (n):
            character = maze_configuration[y][x]
            #Calculate the screen x,y coordinates
            screen_x = -536 + ((((64-n)//2) + x) * 18)
            screen_y = 536 - ((((64-n)//2)+ y) * 18)
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
            screen_x = -536 + ((((64-n)//2) + x )* 18)
            screen_y = 536 - ((((64-n)//2)+y) * 18)
            #Check if it is an X (representing a wall)
            if character == "*":
                path.goto(screen_x, screen_y)
                path.showturtle()
                path.stamp()
            
            if character == "o":
                player.goto(screen_x, screen_y)
                player.stamp()

wall = Icon()
player = Player()
path = Path()
goal = Goal()
turtle.exitonclick()

