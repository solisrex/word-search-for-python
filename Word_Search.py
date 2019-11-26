import pygame, sys, random, string, math
from pygame.locals import *

pygame.init()
width = 750
height = 750
DISPLAYSURF =  pygame.display.set_mode((width,height))

fontObj = pygame.font.SysFont('calibri', 32)
grid_width = 15
grid_height = 15
chars =  [[[random.choice(string.ascii_uppercase),False,False] for a in range(grid_width)] for b in range(grid_height)]

words = sys.argv[1:]

words = [word.upper() for word in words]

def place_word(word):
    direction = random.choice([0,1,2,3])
    place = True
    if direction == 0:
        startx, starty = random.choice(range(grid_width-len(word))),random.choice(range(grid_height))
        for i in range(len(word)):
            if chars[starty][startx+i][1] == True and chars[starty][startx+i][0] != word[i]:
                place = False
        if place == True:
            for i in range(len(word)):
                chars[starty][startx+i]=[word[i],True,False]
    elif direction == 1:
        startx, starty = random.choice(range(grid_width)),random.choice(range(grid_height-len(word)))
        for i in range(len(word)):
            if chars[starty+i][startx][1] == True and chars[starty+i][startx][0] != word[i]:
                place = False
        if place == True:
            for i in range(len(word)):
                chars[starty+i][startx]=[word[i],True,False]
    elif direction == 2:
        startx, starty = random.choice(range(grid_width-len(word))),random.choice(range(len(word),grid_height))
        for i in range(len(word)):
            if chars[starty-i][startx+i][1] == True and chars[starty-i][startx+i][0] != word[i]:
                place = False
        if place == True:
            for i in range(len(word)):
                chars[starty-i][startx+i]=[word[i],True,False]
    elif direction == 3:
        startx, starty = random.choice(range(grid_width-len(word))),random.choice(range(grid_height-len(word)))
        for i in range(len(word)):
            if chars[starty+i][startx+i][1] == True:
                if chars[starty+i][startx+i][0] != word[i]:
                    place = False
        if place == True:
            for i in range(len(word)):
                chars[starty+i][startx+i]=[word[i],True,False]
    return place

for word in words:
    count = 0
    while place_word(word) == False and count < 1000:
        count += 1

def draw_selection(startx,starty,endx,endy):
    if starty < endy and (startx!=endx or starty!=endy):
        angle = math.acos((startx-endx)/math.sqrt((endx-startx)**2+(endy-starty)**2))
    elif (startx!=endx or starty!=endy):
        angle = -math.acos((startx-endx)/math.sqrt((endx-startx)**2+(endy-starty)**2))
    else:
        angle=0
    pygame.draw.arc(DISPLAYSURF,(16,45,42),(startx*width//grid_width+width//(5*grid_width),starty*height//grid_height+height//(5*grid_height),width//grid_width-2*width//(5*grid_width),height//grid_height-2*height//(5*grid_height)),angle-math.pi/2,angle+math.pi/2,3)
    pygame.draw.arc(DISPLAYSURF,(16,45,42),(endx*width//grid_width+width//(5*grid_width),endy*height//grid_height+height//(5*grid_height),width//grid_width-2*width//(5*grid_width),height//grid_height-2*height//(5*grid_height)),angle+math.pi/2,angle-math.pi/2,3)
    pygame.draw.line(DISPLAYSURF,(16,45,42),((startx+1/2)*width//grid_width+(width//grid_width-2*width//(5*grid_width))//2*math.cos(angle+math.pi/2),(starty+1/2)*height//grid_height-(height//grid_height-2*height//(5*grid_height))//2*math.sin(angle+math.pi/2)),((endx+1/2)*width//grid_width+(width//grid_width-2*width//(5*grid_width))//2*math.cos(angle+math.pi/2),    (endy+1/2)*height//grid_height-(height//grid_height-2*height//(5*grid_height))//2*math.sin(angle+math.pi/2)),3)
    pygame.draw.line(DISPLAYSURF,(16,45,42),((startx+1/2)*width//grid_width+(width//grid_width-2*width//(5*grid_width))//2*math.cos(angle-math.pi/2),(starty+1/2)*height//grid_height-(height//grid_height-2*height//(5*grid_height))//2*math.sin(angle-math.pi/2)),((endx+1/2)*width//grid_width+(width//grid_width-2*width//(5*grid_width))//2*math.cos(angle-math.pi/2),(endy+1/2)*height//grid_height-(width//grid_width-2*width//(5*grid_width))//2*math.sin(angle-math.pi/2)),3)

def main():
    FPSCLOCK = pygame.time.Clock()
    selecting = False
    while True:
        DISPLAYSURF.fill((161,234,227))
        for i, j in [[a,b] for a in range(grid_height) for b in range(grid_width)]:
            char = chars[i][j][0]
            color = chars[i][j][2]
            if color == False:
                text = fontObj.render(str(char), True, (16,45,42))
            else:
                text = fontObj.render(str(char), True, (242,78,46))
            w, h = text.get_width(), text.get_height()
            DISPLAYSURF.blit(text,((j+1/2)*width//grid_width-w//2,(i+1/2)*height//grid_height-h//2))
        if selecting:
            draw_selection(selx,sely,gridx,gridy)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if selecting:
                    newx, newy = mousex*grid_width//width, mousey*grid_height//height
                    if (newx==selx):
                        gridx, gridy = newx, newy
                    elif (newy==sely):
                        gridx, gridy = newx, newy
                    elif (newx-selx==sely-newy):
                        gridx, gridy = newx, newy
                    elif (newx-selx==newy-sely):
                        gridx, gridy = newx, newy
            if event.type ==  MOUSEBUTTONUP:
                selecting = not selecting
                if selecting:
                    selx, sely = mousex*grid_width//width, mousey*grid_height//height
                    gridx, gridy = selx, sely
                else:
                    if (gridx==selx):
                        if sely > gridy:
                            word = "".join([chars[gridy+i][selx][0] for i in range(sely-gridy+1)])
                            if word in words:
                                for i in range(sely-gridy+1):
                                    chars[gridy+i][selx][2] = True
                        else:
                            word = "".join([chars[sely+i][selx][0] for i in range(gridy-sely+1)])
                            if word in words:
                                for i in range(gridy-sely+1):
                                    chars[sely+i][selx][2] = True
                    elif (gridy==sely):
                        if selx > gridx:
                            word = "".join([chars[sely][gridx+i][0] for i in range(selx-gridx+1)])
                            if word in words:
                                for i in range(selx-gridx+1):
                                    chars[sely][gridx+i][2] = True
                        else:
                            word = "".join([chars[sely][selx+i][0] for i in range(gridx-selx+1)])
                            if word in words:
                                for i in range(gridx-selx+1):
                                    chars[sely][selx+i][2] = True
                    elif (gridx-selx==sely-gridy):
                        if selx > gridx:
                            word = "".join([chars[gridy-i][gridx+i][0] for i in range(selx-gridx+1)])
                            if word in words:
                                for i in range(selx-gridx+1):
                                    chars[gridy-i][gridx+i][2] = True
                        else:
                            word = "".join([chars[sely-i][selx+i][0] for i in range(gridx-selx+1)])
                            if word in words:
                                for i in range(gridx-selx+1):
                                    chars[sely-i][selx+i][2] = True
                    elif (gridx-selx==gridy-sely):
                        if selx > gridx:
                            word = "".join([chars[gridy+i][gridx+i][0] for i in range(selx-gridx+1)])
                            if word in words:
                                for i in range(selx-gridx+1):
                                    chars[gridy+i][gridx+i][2] = True
                        else:
                            word = "".join([chars[sely+i][selx+i][0] for i in range(gridx-selx+1)])
                            if word in words:
                                for i in range(gridx-selx+1):
                                    chars[sely+i][selx+i][2] = True
                    
        pygame.display.update()
        FPSCLOCK.tick(5)


main()
