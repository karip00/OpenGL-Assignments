from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# import math

WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600
ripple_count = 0


circleList = []

# draws the points in all zones - correctly written
def circ_point(x, y, cx, cy):

    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)



# calls circ_point and draws the circle acc to given values
def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius

    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y = y - 1
        x = x + 1
        circ_point(x, y, cx, cy)

# initializes the viewmatrix
def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


paused = False
# un/pauses the game if spacebar is pressed - uses paused flag
def keyboard_ordinary_keys(key, _, __):
    global paused
    if key == b' ':
        paused = not(paused)        
    glutPostRedisplay()


customFactor = 1
# inc/decreases the speed of the ripple if left/right arrow is pressed - uses customFactor
def keyboard_special_keys(key, _, __):
    global customFactor
    if customFactor <= 0:
            customFactor = 0

    if key == GLUT_KEY_LEFT:
        customFactor += 0.1

    elif key == GLUT_KEY_RIGHT:
        customFactor -= 0.1
    
    print(f"Custom Factor: {customFactor}")


    # print(customFactor)
    glutPostRedisplay()
    

incFactor = 2
# generates new circle - decreases the radius increment rate with the creation of multiple circles - uses incFactor
def mouse_click(button, state, x, y):
    global WINDOW_HEIGHT, ripple_count, circleList, incFactor, paused

    if paused == False:

        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            
            circleList.append([x, WINDOW_HEIGHT-y, 0])
            ripple_count += 1
            incFactor -= 0.04

            print(f"number of ripples: {ripple_count}")
            print(f"Increment Factor: {incFactor}")
            glutPostRedisplay()


    
def animation():
    global circleList, ripple_count, incFactor, paused, customFactor, WINDOW_WIDTH, WINDOW_HEIGHT

    if paused == False:
        x_min, x_max = 0, WINDOW_WIDTH
        y_min, y_max = 0, WINDOW_HEIGHT


        if customFactor <= 0:
            customFactor = 0

        for circle in circleList:

            a = circle[0]
            b = circle[1]
            r = circle[2]

            circle[2] = (circle[2] + incFactor*customFactor) % 600


            if circle[2] > 590:
            # if not((a-r) > x_min and (a+r) > x_max and (b-r) > y_min and (b+r) > y_max):
                circleList = circleList[1:]
                # print(1)
                # circleList.remove(circle)
                ripple_count -= 1
                incFactor += 0.04

                print(f"number of ripples: {ripple_count}")
    glutPostRedisplay()

def show_screen():
    global circleList

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor3f(0.447, 1.0, 0.973)
    glPointSize(2)
    glBegin(GL_POINTS)

    # mid_circle(350, 350, radius)
    # mid_circle(350, 400, radius)
    for x, y, r in circleList:
        mid_circle(x, y, r)

    glEnd()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Circles")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)
# glutIdleFunc(show_screen)

glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()

#save everytime after change, otherwise kaaj korbe na