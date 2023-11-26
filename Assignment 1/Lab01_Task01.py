from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

def pointsGen():
    random_points = []
    for i in range(250):
        random_points.append((int(random.uniform(0,500)),int(random.uniform(0,500))))
    return random_points



def draw_points(x, y):
    glPointSize(1) #size of the pixel, by default 1
    glBegin(GL_POINTS) #glBegin takes shape as parameters, like points, triangles or lines etc. -- glBegin(GL_*mode*)
    glVertex2f(x,y) #coord on which the pixel will be shown, specified upto 2floating point values
    glEnd()

def draw_line(x1, y1, x2, y2):
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def rain(x1, y1, x2, y2):
    global windDirection
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(x1+windDirection, y1)
    glVertex2f(x2+windDirection, y2)
    glEnd()

#function for drawing
def iterate():

    #setting up the viewport and projection
    glViewport(0, 0, 500, 500)   #dimensions of the viewport, (0,0) refers to the lowest corner, (500,500) refers to 500px tall and 500px wide
    glMatrixMode(GL_PROJECTION)  #sets the matrixmode to projection mode, which converts 3d objects to 2d space for rendering
    glLoadIdentity()             #resets the current matrixmode to identity matrix, to use the matrix for diff purpose
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)  #specifies  viewing box of dims. of 500unit in width and height, and a depth of 1 unit
    glMatrixMode (GL_MODELVIEW)  #sets the matrix to modelview mode, which transform object coords to eye coords
    glLoadIdentity()

def keyboardListener(key, x, y):
    global backgColor, lineColor
    if key == b'd':
        backgColor = [0.0, 0.0, 0.0, 0.0]
        lineColor = [1.0, 1.0, 1.0, 1.0]
        print('dark mode enabled')
    elif key == b'l':
        backgColor = [1.0, 1.0, 1.0, 1.0]
        lineColor = [0.0, 0.0, 0.0, 0.0]
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    glutPostRedisplay()

def specialKeyListener(key,x,y):
    global windDirection

    if key == GLUT_KEY_RIGHT:
        windDirection = 0.5
        print("->")
    elif key == GLUT_KEY_LEFT:
        windDirection = -0.5
        print("<-")
    elif key == GLUT_KEY_DOWN:
        windDirection = 0
        print("RESET")


rain_lines = pointsGen()
backgColor = [0.0, 0.0, 0.0, 0.0]
lineColor = [1.0, 1.0, 1.0, 1.0]
windDirection = 0

#all about the DRAWING
def showScreen():

    global rain_lines, backgColor, lineColor, windDirection

    #clear the screen
    r1 = backgColor[0]
    g1 = backgColor[1]
    b1 = backgColor[2]
    glClearColor(*backgColor)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #Clears the color and depth buffers,to clear the previous scene
    glLoadIdentity()

    #goes to iterate func
    iterate()

    #sets te color to red
    r2 = lineColor[0]
    g2 = lineColor[1]
    b2 = lineColor[2]
    glColor3f(r2,g2,b2) #color set (R,G,B) - 0/1

    #call the draw methods here

    #drawing the house
    draw_line(100,50,400,50)
    draw_line(100, 50, 100, 250)
    draw_line(300, 50, 300, 250)
    draw_line(90, 250, 310, 250)
    draw_line(90, 260, 310, 260)
    draw_line(90, 250, 90, 260)
    draw_line(310, 250, 310, 260)
    draw_line(300, 150, 410, 150)
    draw_line(300, 160, 410, 160)
    draw_line(410, 150, 410, 160)
    draw_line(400, 50, 400, 150)
    draw_line(175, 50, 175, 100)
    draw_line(225, 50, 225, 100)
    draw_line(375, 50, 375, 100)
    draw_line(325, 50, 325, 100)
    draw_line(175, 100, 225, 100)
    draw_line(325, 100, 375, 100)
    draw_line(100,260, 200, 350)
    draw_line(200, 350, 300, 260)

    for i in range(len(rain_lines)):
        x1, y1 = rain_lines[i]
        y2 = y1 - random.uniform(5, 15)  # random length of the raindrop
        rain(x1, y1, x1, y2)

        # update the position of the raindrop
        if y1 < -5:
            y1 = random.uniform(500, 550)  # if the raindrop has fallen below the window then take it back to the top
            x1 = random.uniform(0, 500)  # reset x-coordinate as well
        else:
            y1 -= random.uniform(1, 2)  # else keep decreasing the y coordinate
            x1 += windDirection  # add wind direction to x-coordinate

        rain_lines[i] = (x1, y1)

    glutSwapBuffers()
#################################################




#######################################################
### all about the WINDOW
glutInit()   #initiates the GLUT library
glutInitDisplayMode(GLUT_RGBA)   #selects initial display mode, selects an RGBA mode window
glutInitWindowSize(500, 500)   #sets the size of the window
glutInitWindowPosition(0, 0)   #sets the initial window position
wind = glutCreateWindow(b"Task 1") #title of the window
glutDisplayFunc(showScreen)   #sets the display callback which draws everything on the screen
glutIdleFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()   #event processing loop which does not return until the program is terminated
