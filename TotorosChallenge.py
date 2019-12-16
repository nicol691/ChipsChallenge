# Totoros Challenge
# By Nicole Brown

import random, pygame, sys, time
from pygame.locals import *

BOARDSIZE=18 
FPS = 32 # frames per second, the general speed of the program
WINDOWWIDTH = 1000 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 30 # size of box height & width in pixels
GAPSIZE = 2 # size of gap between boxes in pixels
BOARDWIDTH = BOARDSIZE # number of columns of icons
BOARDHEIGHT = BOARDSIZE # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2 - 200)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
AQUA     = (0, 255, 255)
BLACK = (8 ,8 ,8)
BRIGHTGREEN = (127,255,0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = RED

EMPTY = 'empty'
WALL = 'wall'
WATER = 'water'
FIRE = 'fire'
ICE = 'ice'
BLOCK = 'block'
BUTTON = 'button'
BUTTONDOOR = 'buttondoor'
KEYDOOR = 'keydoor'
KEY = 'key'
HEART = 'heart'
ENDDOOR = 'enddoor'
TOTORO = 'totoro'
HINTBOX1 = 'hintbox1'
HINTBOX2 = 'hintbox2'
HINTBOX3 = 'hintbox3'
HINTBOX4 = 'hintbox4'
HINTBOX5 = 'hintbox5'
HINTBOX6 = 'hintbox6'
HINTBOX7 = 'hintbox7'
HINTBOX8 = 'hintbox8'
MONSTER = 'monster'
CHIP = 'chip'
WATERBOOT = 'waterboot'
FIREBOOT = 'fireboot'
ICESKATES = 'iceskates'
pygame.init()

#add music
#pygame.mixer.music.load('minemusic.wav')
#pygame.mixer.music.play(-1)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

Level = 1

TotoroX = 1
TotoroY = 1
Monster = []
hasWaterBoots = False
hasIceSkates = False
hasKey = False
hasFireBoots = False
pressButton = False
hasHeart = False
chipcounter = 0
heartcounter = 0
score = 0
ResetLevel = False
LevelTime = [0, 120, 60, 60]

def main():
    global FPSCLOCK, DISPLAYSURF, TotoroX, TotoroY, hasWaterBoots, hasIceSkates, hasKey, hasFireBoots, pressButton, hasHeart, Level, chipcounter
    global heartcounter, score, ResetLevel
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    Counter = 0
    PreviousLevelScore = 0
    Time = LevelTime[Level]
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Totoros Challenge')

    mainBoard = getBoard(Level)
     
    pygame.display.update()

    DISPLAYSURF.fill(BGCOLOR)

    GameRunning = True
    updateBoard = True
    while True: # main game loop
        FPSCLOCK.tick(FPS)

        Counter = Counter + 1
        if Counter % FPS == 0:
            Time = Time - 1
            if Time <= 0:
                Time = 0
                GameRunning = False
                
        DISPLAYSURF.fill(BGCOLOR) # drawing the window

 
            
        #ENDDOOR
        if mainBoard[TotoroX][TotoroY] == ENDDOOR:
            GoToNextLevel = False
            if Level == 1 and heartcounter == 2 and chipcounter == 6:
                GoToNextLevel = True
            elif Level == 2 and heartcounter == 4 and chipcounter == 16:
                GoToNextLevel = True
            elif Level == 3 and heartcounter == 7 and chipcounter == 33:
                GameRunning = False
            if GoToNextLevel:
                if hasHeart:
                    score = score + 100
                PreviousLevelScore = score
                Level = Level + 1
                Time = LevelTime[Level]
                mainBoard = getBoard(Level)
                resetItems()

        if ResetLevel:
            Time = LevelTime[Level]
            score = PreviousLevelScore
            mainBoard = getBoard(Level)
            resetItems()
            if Level == 1:
                heartcounter = 0
                chipcounter = 0
            if Level == 2:
                heartcounter = 2
                chipcounter = 6
            if Level == 3:
                heartcounter = 4
                chipcounter = 16
        
        if updateBoard or Counter % FPS == 0:
            message_display('Time:', 628, 25)
            message_display(str(Time), 800, 25)

            message_display('Score:', 632, 50)
            message_display(str(score), 800, 50)
            
            message_display('Chips collected:', 671, 125)
            message_display(str(chipcounter), 800, 125)
            
            message_display('Total Hearts collected:', 668, 100)
            message_display(str(heartcounter), 800, 100)
            
            message_display('Has heart:', 647, 150)
            message_display(str(hasHeart), 800, 150)
            
            message_display('Has fireboots:', 661, 175)
            message_display(str(hasFireBoots), 800, 175)
            
            message_display('Has key:', 640, 200)
            message_display(str(hasKey), 800, 200)
            
            message_display('Has waterboots:', 670, 225)
            message_display(str(hasWaterBoots), 800, 225)
            
            message_display('Has iceskates:', 662, 250)
            message_display(str(hasIceSkates), 800, 250)

            if not GameRunning:
                message_display('GAME OVER', 800, 400)

            if ResetLevel:
                message_display('RESET LEVEL: MONSTER KILLED YOU', 800, 400)
            
            drawBoard(mainBoard)
            pygame.display.update()
            updateBoard = False

            if ResetLevel:
                ResetLevel = False
                time.sleep(5)

           
            
       
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and GameRunning:
                updateBoard = True
                # check if the user pressed a key to move Totoro
                if event.key in (K_LEFT, K_a) and ValidMove(mainBoard, LEFT):
                    TotoroY = TotoroY - 1
                elif event.key in (K_RIGHT, K_d) and ValidMove(mainBoard, RIGHT):
                    TotoroY = TotoroY + 1
                elif event.key in (K_UP, K_w) and ValidMove(mainBoard, UP):
                    TotoroX = TotoroX - 1
                elif event.key in (K_DOWN, K_s) and ValidMove(mainBoard, DOWN): 
                    TotoroX = TotoroX + 1

        if not GameRunning:
            continue

        #Make Monster move
        if Counter % 32 == 0:
            MonsterNo = 0
            for MonsterPos in Monster:
                if Level == 1:
                    if MonsterNo == 0:
                        newPos = MonsterPos[0]+MonsterPos[2]
                        if (TotoroX == newPos and TotoroY == MonsterPos[1]):
                            if hasHeart:
                                hasHeart = False
                            else:
                                ResetLevel = True
                        if newPos>=0 and newPos<BOARDWIDTH and mainBoard[newPos][MonsterPos[1]] != WALL:
                            MonsterPos[0] = newPos
                            updateBoard = True
                        else:
                            MonsterPos[2] = -MonsterPos[2] #Change monster direction
                    if MonsterNo == 1:
                        if (TotoroX == MonsterPos[0] and TotoroY == newPos):
                            if hasHeart:
                                hasHeart = False
                            else:
                                ResetLevel = True
                        newPos = MonsterPos[1] + MonsterPos[2]
                        if newPos>=0 and newPos<BOARDWIDTH and mainBoard[MonsterPos[0]][newPos] != WALL:
                            MonsterPos[1] = newPos
                            updateBoard = True
                        else:
                            MonsterPos[2] = -MonsterPos[2] #Change monster direction
                MonsterNo = MonsterNo + 1
        if Counter % 8 == 0:
           MonsterNo = 0
           for MonsterPos in Monster:
               if Level == 2:
                        newPos = MonsterPos[1] + MonsterPos[2]
                        if (TotoroX == MonsterPos[0] and TotoroY == newPos):
                            if hasHeart:
                                hasHeart = False
                            else:
                                ResetLevel = True
                        if newPos>=0 and newPos<BOARDWIDTH and mainBoard[MonsterPos[0]][newPos] != WALL:
                            MonsterPos[1] = newPos
                            updateBoard = True
                        else:
                            MonsterPos[2] = -MonsterPos[2] #Change monster direction
        if Counter % 6 == 0:
           MonsterNo = 0
           for MonsterPos in Monster:
               if Level == 3:
                    if MonsterNo == 0:
                        newPos = MonsterPos[0]+MonsterPos[2]
                        if (TotoroX == newPos and TotoroY == MonsterPos[1]):
                            if hasHeart:
                                hasHeart = False
                            else:
                                ResetLevel = True
                        if newPos>=0 and newPos<BOARDWIDTH and mainBoard[newPos][MonsterPos[1]] != WALL:
                            MonsterPos[0] = newPos
                            updateBoard = True
                        else:
                            MonsterPos[2] = -MonsterPos[2] #Change monster direction
                    if MonsterNo == 1:
                        newPos = MonsterPos[1] + MonsterPos[2]
                        if (TotoroX == MonsterPos[0] and TotoroY == newPos):
                            if hasHeart:
                                hasHeart = False
                            else:
                                ResetLevel = True
                        if newPos>=0 and newPos<BOARDWIDTH and mainBoard[MonsterPos[0]][newPos] != WALL:
                            MonsterPos[1] = newPos
                            updateBoard = True
                        else:
                            MonsterPos[2] = -MonsterPos[2] #Change monster direction
               MonsterNo = MonsterNo + 1

def resetItems():
    global hasWaterBoots, hasIceSkates, hasKey, hasFireBoots, hasHeart
    hasWaterBoots = False
    hasIceSkates = False
    hasKey = False
    hasFireBoots = False
    hasHeart = False

       
def getBoard(level):
    global TotoroX, TotoroY, Monster
    board = []
    myfile = 'Level'+str(level)+'.txt'
    with open(myfile, 'r') as fileobj:
      for line in fileobj:
        lineBox = []
        for ch in line:
          if ch == 'h':
            lineBox.append(WALL)
          elif ch == 's':
            lineBox.append(EMPTY)
          elif ch == 'f':
            lineBox.append(FIRE)
          elif ch == 'w':
              lineBox.append(WATER)
          elif ch == 'i':
              lineBox.append(ICE)
          elif ch == 'b':
              lineBox.append(BLOCK)
          elif ch == 'm':
              lineBox.append(BUTTONDOOR)
          elif ch == 'k':
              lineBox.append(KEYDOOR)
          elif ch == 'l':
              lineBox.append(HEART)
          elif ch == 'p':
              lineBox.append(BUTTON)
          elif ch == 'n':
              lineBox.append(KEY)
          elif ch == 'e':
              lineBox.append(ENDDOOR)
          elif ch == 't':
              lineBox.append(TOTORO)
          elif ch == '1':
              lineBox.append(HINTBOX1)
          elif ch == '2':
              lineBox.append(HINTBOX2)
          elif ch == '3':
              lineBox.append(HINTBOX3)
          elif ch == '4':
              lineBox.append(HINTBOX4)
          elif ch == '5':
              lineBox.append(HINTBOX5)
          elif ch == '6':
              lineBox.append(HINTBOX6)
          elif ch == '7':
              linBox.append(HINTBOX7)
          elif ch == '8':
              lineBox.append(HINTBOX8)  
          elif ch == 'z':
              lineBox.append(MONSTER)
          elif ch == 'c':
              lineBox.append(CHIP)
          elif ch == 'y':
              lineBox.append(WATERBOOT)
          elif ch == 'a':
              lineBox.append(FIREBOOT)
          elif ch == 'g':
              lineBox.append(ICESKATES)
          elif ch == "q":
              lineBox.append(EMPTY) #What is q for?
          else:
              print("Not found: ", ch)

        board.append(lineBox)

    Monster = []
    
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxy][boxx] == TOTORO:
                TotoroX = boxy
                TotoroY = boxx
            if board[boxy][boxx] == MONSTER:
                Monster.append([boxy, boxx, 1])

    if Level == 1:
        pygame.mixer.music.load('star.wav')
        pygame.mixer.music.play(-1)
    if Level == 2:
        pygame.mixer.music.load('intro.mp3')
        pygame.mixer.music.play(-1)
    if Level == 3:
        pygame.mixer.music.load('Ipsi.mp3')
        pygame.mixer.music.play(-1)


    return board


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def ValidMove(board, direction): #check if Totoro can move
    global hasWaterBoots, hasIceSkates, hasKey, hasFireBoots, pressButton, hasHeart, chipcounter, heartcounter, score, ResetLevel
    if direction == UP:
        boxx = TotoroX - 1
        boxy = TotoroY
    if direction == DOWN:
        boxx = TotoroX + 1
        boxy = TotoroY
    if direction == LEFT:
        boxx = TotoroX
        boxy = TotoroY - 1
    if direction == RIGHT:
        boxx = TotoroX
        boxy = TotoroY + 1
        
    if boxx < 0 or boxx >= BOARDWIDTH:
        return False
    if boxy < 0 or boxy >= BOARDHEIGHT:
        return False
#WALL
    if board[boxx][boxy] == WALL:
        return False
#WATERBOOT & WATER
    if board[boxx][boxy] == WATERBOOT:
        hasWaterBoots = True
        board[boxx][boxy] = EMPTY
        return True
    if board[boxx][boxy] == WATER:
        return hasWaterBoots
    
#ICESKATES & ICE
    if board[boxx][boxy] == ICESKATES:
        hasIceSkates = True
        board[boxx][boxy] = EMPTY
        return True
    if board[boxx][boxy] == ICE:
        return hasIceSkates

#FIREBOOT & FIRE
    if board[boxx][boxy] == FIREBOOT:
        hasFireBoots = True
        board[boxx][boxy] = EMPTY
        return True
    if board[boxx][boxy] == FIRE:
        return hasFireBoots

#HEART & MONSTER
    if board[boxx][boxy] == HEART:
        hasHeart = True
        heartcounter = heartcounter+1
        score = score + 20
        print("HEART", heartcounter)
        board[boxx][boxy] = EMPTY
        return True

    for MonsterPos in Monster:
        if boxx == MonsterPos[0] and boxy == MonsterPos[1]:
            if hasHeart == True:
                hasHeart = False
                return True
            else:
                ResetLevel = True
                return False
        
#CHIP
    if board[boxx][boxy] == CHIP:
        chipcounter = chipcounter+1
        score = score + 10
        print("CHIP", chipcounter)
        board[boxx][boxy] = EMPTY
        return True
    
#BUTTON AND BUTTONDOOR
    if board[boxx][boxy] == BUTTON:
        pressButton = True
        board[boxx][boxy] = EMPTY
        return True
    if board[boxx][boxy] == BUTTONDOOR:
        if pressButton == True:
            pressButton = False
            board[boxx][boxy] = EMPTY
            return True
        else:
            return False
        
#KEY AND KEYDOOR
    if board[boxx][boxy] == KEY:
        hasKey = True
        board[boxx][boxy] = EMPTY
        return True     
    if board[boxx][boxy] == KEYDOOR:
        if hasKey == True:
            hasKey = False
            board[boxx][boxy] = EMPTY
            return True
        else:
            return False


        
    if board[boxx][boxy] == BLOCK:
        if direction == UP:
            if boxx-1 < 0:
                return False
            if board[boxx-1][boxy] == EMPTY:
                board[boxx-1][boxy] = BLOCK
                board[boxx][boxy] = EMPTY
                return True
            else:
                return False
        if direction == DOWN:
            if boxx+1 >= BOARDWIDTH:
                return False
            if board[boxx+1][boxy] == EMPTY:
                board[boxx+1][boxy] = BLOCK
                board[boxx][boxy] = EMPTY
                return True
            else:
                return False

        if direction == LEFT:
            if boxy-1 < 0:
                return False
            if board[boxx][boxy-1] == EMPTY:
                board[boxx][boxy-1] = BLOCK
                board[boxx][boxy] = EMPTY
                return True
            else:
                return False
        if direction == RIGHT:
            if boxy+1 >= BOARDHEIGHT:
                return False
            if board[boxx][boxy+1] == EMPTY:
                board[boxx][boxy+1] = BLOCK
                board[boxx][boxy] = EMPTY
                return True
            else:
                return False
    return True
    
       
        
def drawBoard(board):
    half =    int(BOXSIZE * 0.5)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxy][boxx] == EMPTY:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == WALL:
                pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == FIRE:
                pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))
                Ima = pygame.image.load("fire.png")
                DISPLAYSURF.blit(Ima,(left,top))
            elif board[boxy][boxx] == WATER:
                pygame.draw.rect(DISPLAYSURF, BLUE, (left, top, BOXSIZE, BOXSIZE))
                I = pygame.image.load("water.png")
                DISPLAYSURF.blit(I,(left,top))
            elif board[boxy][boxx] == ICE:
                pygame.draw.rect(DISPLAYSURF, AQUA, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("ice1.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == BLOCK:
                pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == KEYDOOR:
                pygame.draw.rect(DISPLAYSURF, YELLOW, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == BUTTONDOOR:
                pygame.draw.rect(DISPLAYSURF, PURPLE, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == ENDDOOR:
                pygame.draw.rect(DISPLAYSURF, BRIGHTGREEN, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxy][boxx] == KEY:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                GameImage = pygame.image.load("key1.png")
                DISPLAYSURF.blit(GameImage,(left,top))
            elif board[boxy][boxx] == BUTTON:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("button.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == TOTORO:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                #Image = pygame.image.load("Totoro.png")
                #DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == HINTBOX1:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("hint.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == HINTBOX2:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("hint.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == HINTBOX3:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("hint.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == HINTBOX4:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("hint.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == MONSTER:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                #Image = pygame.image.load("monster.png")
                #DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == CHIP:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("chip.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == WATERBOOT:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("waterboot.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == FIREBOOT:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("fireboot.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == ICESKATES:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("iceskates.png")
                DISPLAYSURF.blit(Image,(left,top))
            elif board[boxy][boxx] == HEART:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("heart.png")
                DISPLAYSURF.blit(Image,(left,top))
            if boxx == TotoroY and boxy == TotoroX:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("Totoro.png")
                Image = pygame.Surface([0,0], pygame.SRCALPHA, 32)
                Image = Image.convert_alpha()
                #Image = pygame.image.load("Totoro.png").convert_alpha()
                #DISPLAYSURF.blit(Image,(left,top))
            for MonsterPos in Monster:
                if MonsterPos[1] == boxx and MonsterPos[0] == boxy:
                    pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                    Image = pygame.image.load("monster.png")
                    DISPLAYSURF.blit(Image,(left,top))   
            if boxx == TotoroY and boxy == TotoroX:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                Image = pygame.image.load("Totoro.png").convert_alpha()
                DISPLAYSURF.blit(Image,(left,top))    
            if board[boxy][boxx] == HINTBOX1:
                if TotoroY == boxx and TotoroX == boxy:
                    message_display('Get water slipper to walk on water', 733, 300)
                    #message_display('to walk on water.', 700, 260)
            if board[boxy][boxx] == HINTBOX2:
                if TotoroY == boxx and TotoroX == boxy:
                    message_display('Get heart to pass monster.', 704, 300)
                    message_display('You can only use the heart one time. After you use it,', 797, 325)
                    message_display('you will not be able to pass the monster again', 774, 350)
            if board[boxy][boxx] == HINTBOX3:
                if TotoroY == boxx and TotoroX == boxy:
                    message_display('Get yellow key to get pass the yellow block',745, 300)
                    #message_display('to walk on water.', 700, 260)
            if board[boxy][boxx] == HINTBOX4:
                if TotoroY == boxx and TotoroX == boxy:
                    message_display('Get fireboot to walk on fire.', 774, 350)
                

                
def message_display(text, left, top):
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (left,top)
    DISPLAYSURF.blit(TextSurf, TextRect)
    #pygame.display.update()

def text_objects(text, font):
    textSurface = font.render(text, True, CYAN)
    return textSurface, textSurface.get_rect()
    
if __name__ == '__main__':
    main()


    
    
