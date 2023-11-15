from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

def drawPixel(x, y, color):
    glPointSize(1)
    glBegin(GL_POINTS)
    glColor3fv(color)
    glVertex2f(x,y)
    glEnd()

#find zone for MPL
def findZone(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6
    
    return zone

#converts to zone 0
def convertZone(x, y, zone):

    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y
        
#revert to required zone
def revertZone(x, y, zone):

    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:
        return x, -y

#draw line using MPL
def drawLine(x1, y1, x2, y2, color):

    dx = x2 - x1
    dy = y2 - y1
    zone = findZone(x1, y1, x2, y2)

    if zone != 0:
        x1, y1, x2, y2 = convertZone(x1, y1, zone)[0], convertZone(x1, y1, zone)[1], convertZone(x2, y2, zone)[0], convertZone(x2, y2, zone)[1]
        dy = y2 - y1
        dx = x2 - x1

        
    d = (2*dy) - dx
    incE = 2*dy
    incNE = 2*(dy - dx)
    
    x = x1
    y = y1

    while x <= x2 and y <= y2:
        drawPixel(revertZone(x, y, zone)[0], revertZone(x, y, zone)[1],color)
        if d < 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
        

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and # x_min_1 < x_max_2
                self.x + self.w > other.x  and # x_max_1 > m_min_2
                self.y < other.y + other.h and # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2


#spawns the diamond
dcolor = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
def spawnDiamond(x_start, y_start):
    global dcolor
    clr = dcolor
    upX, upY = x_start, y_start
    leftX, leftY = upX-10, upY-10
    rightX, rightY = upX+10, upY-10
    downX, downY = upX, upY-20
    drawLine(upX, upY, leftX, leftY, clr)
    drawLine(upX, upY, rightX, rightY, clr)
    drawLine(downX, downY, leftX, leftY, clr)
    drawLine(downX, downY, rightX, rightY, clr)

#thalabati
def thalabati(x, y, color):
    tlX, tlY = x, y
    trX, trY = x + 100, y
    blX, blY = x + 10, 10
    brX, brY = x + 90, 10
    if color == 'red':
        drawLine(tlX, tlY, trX, trY, [1,0,0])
        drawLine(tlX, tlY, blX, blY, [1,0,0])
        drawLine(trX, trY, brX, brY, [1,0,0])
        drawLine(blX, blY, brX, brY, [1,0,0])
    else:
        drawLine(tlX, tlY, trX, trY, [1,1,1])
        drawLine(tlX, tlY, blX, blY, [1,1,1])
        drawLine(trX, trY, brX, brY, [1,1,1])
        drawLine(blX, blY, brX, brY, [1,1,1])

def backButton():
    
    drawLine(30,750,70,750, [0,1,1])
    drawLine(30,750,55,770, [0,1,1])
    drawLine(30,750,55,730, [0,1,1])

backBox = AABB(30,730,25,40)

def pauseButton():
    drawLine(250,770,250,730, [1,1,0])
    drawLine(270,770,270,730, [1,1,0])

pauseBox = AABB(230, 730, 60, 40)

def crossButton():
    drawLine(450,770, 480,730, [1,0,0])
    drawLine(480,770,450,730, [1,0,0])

crossBox = AABB(450,730,30,40)

def playButton():
    drawLine(250,770,280,750, [1,1,0])
    drawLine(250,770,250,730, [1,1,0])
    drawLine(250,730,280,750, [1,1,0])

playBox = AABB(230, 730, 60, 40)

def boxClick(key, state, x, y):
    global backBox, pauseBox, crossBox, paused

    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if backBox.x <= x <= (backBox.x+backBox.w) and backBox.y <= (798-y) <= (backBox.y+backBox.h):
            restartGame()
        
        if crossBox.x <= x <= (crossBox.x+crossBox.w) and crossBox.y <= (798-y) <= (crossBox.y+crossBox.h):
            glutLeaveMainLoop()

        if paused == False:
            if pauseBox.x <= x <= (pauseBox.x+pauseBox.w) and pauseBox.y <= (798-y) <= (pauseBox.y+pauseBox.h):
                pauseGame()
        if paused == True:
            if pauseBox.x <= x <= (pauseBox.x+pauseBox.w) and pauseBox.y <= (798-y) <= (pauseBox.y+pauseBox.h):
                playGame()
        

def iterate():

    #setting up the viewport and projection
    glViewport(0, 0, 532, 798)   #dimensions of the viewport, (0,0) refers to the lowest corner, (500,500) refers to 500px tall and 500px wide
    glMatrixMode(GL_PROJECTION)  #sets the matrixmode to projection mode, which converts 3d objects to 2d space for rendering
    glLoadIdentity()             #resets the current matrixmode to identity matrix, to use the matrix for diff purpose
    glOrtho(0.0, 532, 0.0, 798, 0.0, 1.0)  #specifies  viewing box of dims. of 500unit in width and height, and a depth of 1 unit
    glMatrixMode (GL_MODELVIEW)  #sets the matrix to modelview mode, which transform object coords to eye coords
    glLoadIdentity()


dspeed = 1
dspawn_x = int(random.uniform(20,512))
dspawn_y = 810
thala_x = int(random.uniform(0,432))

paused = False
thalabati_position = (0, 0)

def pauseGame():
    global paused, thalabati_position, score, gameOver
    if gameOver == False:
        print("Game Paused")
    paused = not paused


gameOver = False
def restartGame():
    global gameOver, dspawn_x, dspawn_y, dspeed, score, diamondBox, thala_x, thalabatiBox
    gameOver = False
    dspawn_y = 810
    dspawn_x = int(random.uniform(20, 512))
    dspeed = 1
    score = 0
    diamondBox = AABB(dspawn_x-10, dspawn_y-20, 20, 20)
    thala_x = int(random.uniform(0, 432))
    thalabatiBox = AABB(thala_x, 10, 100, 20)

def playGame():
    global paused
    print("Game Resumed")
    paused = False

diamondBox = AABB(dspawn_x-10, dspawn_y-20, 20, 20)
thalabatiBox = AABB(thala_x, 10, 100, 20)

def thalaControl(key,x,y):
    global thala_x, tspeed, thalabatiBox
    if key == GLUT_KEY_RIGHT:
        if thala_x == 422:
            pass
        else:
            thala_x += 20
            thalabatiBox.x += 20
    elif key == GLUT_KEY_LEFT:
        if thala_x == 0:
            pass
        else:
            thala_x -= 20
            thalabatiBox.x -= 20

score = 0
dCoord = [0,0]
def showScreen():
    global dspawn_x, dspawn_y, dspeed, thala_x, diamondBox, thalabatiBox, score, gameOver, paused, thalabati_position, dcolor, dCoord
    glClear(GL_COLOR_BUFFER_BIT)
    iterate()


    if not paused and not gameOver:
        pauseButton()
        dCoord[0] = dspawn_x
        dCoord[1] = dspawn_y
        dspawn_y -= 1*dspeed
        diamondBox.y -= 1*dspeed
        spawnDiamond(dspawn_x, dspawn_y)

        if dspawn_y <= 0:
            gameOver = True
            pauseGame()

            dspawn_y = 810
            dspawn_x = int(random.uniform(20,512))
            dcolor = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
            diamondBox = AABB(dspawn_x-10, dspawn_y-20, 20, 20)

            thalabati(thala_x, 30,'red')

            
            print("Game Over")
            print("Final Score:", score)
            
            
        if diamondBox.collides_with(thalabatiBox):
            dspawn_y = 810
            dspawn_x = int(random.uniform(20,512))
            diamondBox = AABB(dspawn_x-10, dspawn_y-20, 20, 20)
            score += 1
            print("Score: ", score)
        

        if score > 3:
            dspeed = 1.5
            if score > 7:
                dspeed = 2
                if score > 10:
                    dspeed = 3


        thalabati(thala_x, 30, 'white')
        if thala_x < 0:
            thala_x = 0
            thalabatiBox.x = 0
        if thala_x > 422:
            thala_x = 422
            thalabatiBox.x = 422
    
        
    if paused:
        playButton()
        spawnDiamond(dCoord[0], dCoord[1])
        thalabati(thalabati_position[0], thalabati_position[1], 'red')

    backButton()
    
    crossButton()
    
    glutSwapBuffers()




### all about the WINDOW
glutInit()   #initiates the GLUT library
glutInitDisplayMode(GLUT_RGBA)   #selects initial display mode, selects an RGBA mode window
glutInitWindowSize(532, 798)   #sets the size of the window
glutInitWindowPosition(0, 0)   #sets the initial window position
wind = glutCreateWindow(b"Task 1") #title of the window
glutDisplayFunc(showScreen)   #sets the display callback which draws everything on the screen
glutIdleFunc(showScreen)
glutSpecialFunc(thalaControl)
glutMouseFunc(boxClick)
#glutKeyboardFunc(keyboardListener)
glutMainLoop()   #event processing loop which does not return until the program is terminated
