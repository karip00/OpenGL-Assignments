
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

points = []
speed = 0.01
#color = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
#print(color)
#draw function
def drawPoints(x, y, color):
    #global color
    glPointSize(3)
    glBegin(GL_POINTS)
    glColor3f(*color)
    glVertex2f(x, y)
    glEnd()

#mouse function - task2(i + iii)
def mouseInput(key, state, x, y):
    global points, speed
    if key == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            rgb = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
            points.append([x,500-y,speed, rgb])
            #generate point in the screen
            print("Right Click")
    elif key == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            #pixel color change to black
            color = [0, 0, 0]
            print("Left Click")

#freeze function - task2(ii+iv)
freeze = False
def kbInput(key, x, y):
    global points, speed, freeze
    if key==b' ':
        if freeze == False:
            #freeze functionality
            freeze = True
            glutIdleFunc(None)
            print('FREEZE!')
        else:
            freeze = False
            glutIdleFunc(animate)
            print('UNFREEZE')
    elif key == GLUT_KEY_UP:
        #speed increase
        speed += 0.01
        print('SPEED INCREASED')
    elif key == GLUT_KEY_DOWN:
        #speed decrease
        speed -= 0.01
        print('SPEED DECREASED')
    #glutPostRedisplay()

#animate/ update points
def animate():
    global points, speed

    idx = 0
    setList = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
    while idx < len(points):
        points[idx][0] += (random.choice(setList)[0]*speed)
        points[idx][1] += (random.choice(setList)[1]*speed)
        idx += 1

    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global points
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    #glColor3f(1.0, 1.0, 0.0)
    for x, y, s, c in points:
        drawPoints(x, y, c)
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Coding Practice")  #window name
glutDisplayFunc(showScreen)

glutIdleFunc(animate)
glutMouseFunc(mouseInput)
glutKeyboardFunc(kbInput)
glutSpecialFunc(kbInput)
glutMainLoop()