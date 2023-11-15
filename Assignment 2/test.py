def findZone(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx <= 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy <= 0:
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
def drawLine(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1
    zone = findZone(x1, y1, x2, y2)
    #print(x1, y1, x2, y2)
    if zone != 0:
        x1, y1, x2, y2 = convertZone(x1, y1, zone)[0], convertZone(x1, y1, zone)[1], convertZone(x2, y2, zone)[0], convertZone(x2, y2, zone)[1]
        dy = y2 - y1
        dx = x2 - x1
        print(x1, y1, x2, y2)
        
    d = (2*dy) - dx
    incE = 2*dy
    incNE = 2*(dy - dx)

    x = x1
    y = y1

    while x != x2 and y != y2:
        if d < 0:
            d += incE
            if dx != 0:
                x += 1
        else:
            d += incNE
            x += 1
            y += 1
        #print(revertZone(x, y, zone)[0], revertZone(x, y, zone)[1])
        if dx == 0:
            y += 1
        print(revertZone(x, y, zone)[0], revertZone(x, y, zone)[1])

drawLine(60,50,30,50)