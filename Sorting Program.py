import pygame, random, math, time, sys
from pygame.locals import *

#Colours
BLACK      = (   0,   0,   0)
RED        = ( 255,   0,   0)

#Main Variables
FPS = 512
fpsClock = pygame.time.Clock()
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
selected = ''
init = False
passes = 0
count = 0
buffer = 0
comps = 0
pos = 0
swap = False
complete = False
programMode = 0
bars = 50
moveX = WINDOWWIDTH / 15.6
moveY = WINDOWHEIGHT / 32
minPos = 0

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Sorter')
DISPLAYSURF.fill(BLACK)

#Functions
def drawText(surf, text, size, x, y, colour, fontName, method):
    font = pygame.font.Font(pygame.font.match_font(fontName), size)
    TextSurface = font.render(text, True, colour)
    TextRect = TextSurface.get_rect()
    if method == 'mt':
        TextRect.midtop = (x, y)
    elif method == 'c':
        TextRect.center = (x, y)
    surf.blit(TextSurface, TextRect)

#classes
class Button(pygame.sprite.Sprite):
    def __init__(self, X, Y, sizeX):
        self.X = X
        self.Y = Y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((sizeX, WINDOWHEIGHT / 16))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midtop = (X, Y)
        pygame.draw.rect(DISPLAYSURF, RED, self.rect, int(WINDOWWIDTH / 360))

    def update(self, selected, text):
        if text == 'BUBBLE' or text == 'SELECTION' or text == 'INSERTION' or text == 'BOGO' or text == 'MERGE' or text == 'QUICK':
            toggle = True
        else:
            toggle = False
        if pygame.sprite.collide_rect(Mouse, self):
            if not toggle:
                self.image.fill(RED)
                drawText(DISPLAYSURF, text, int(WINDOWHEIGHT / 20), int(self.X), int(self.Y + WINDOWHEIGHT / 120), BLACK, 'calibri', 'mt')
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        elif not selected and not toggle:
            self.image.fill(BLACK)
            pygame.draw.rect(DISPLAYSURF, RED, self.rect, int(WINDOWWIDTH / 360))
            drawText(DISPLAYSURF, text, int(WINDOWHEIGHT / 20), int(self.X), int(self.Y + WINDOWHEIGHT / 120), RED, 'calibri', 'mt')

        if toggle:
            if not selected:
                self.image.fill(BLACK)
                pygame.draw.rect(DISPLAYSURF, RED, self.rect, int(WINDOWWIDTH / 360))
                drawText(DISPLAYSURF, text, int(WINDOWHEIGHT / 20), int(self.X), int(self.Y + WINDOWHEIGHT / 120), RED, 'calibri', 'mt')
            elif selected:
                self.image.fill(RED)
                drawText(DISPLAYSURF, text, int(WINDOWHEIGHT / 20), int(self.X), int(self.Y + WINDOWHEIGHT / 120), BLACK, 'calibri', 'mt')
        return False
        
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

    def update(self, X, Y):
        self.rect.midtop = (X, Y)

#initiation
Mouse = Mouse()
bubbleButton = Button(WINDOWWIDTH / 2, WINDOWHEIGHT / 4, WINDOWHEIGHT / 2.5)
insertionButton = Button(WINDOWWIDTH / 4, WINDOWHEIGHT / 4, WINDOWHEIGHT / 2.5)
selectionButton = Button(WINDOWWIDTH / 4, WINDOWHEIGHT / 3, WINDOWHEIGHT / 2.5)
mergeButton = Button(WINDOWWIDTH / 1.33, WINDOWHEIGHT / 4, WINDOWHEIGHT / 2.5)
quickButton = Button(WINDOWWIDTH / 1.33, WINDOWHEIGHT / 3, WINDOWHEIGHT / 2.5)
bogoButton = Button(WINDOWWIDTH / 2, WINDOWHEIGHT / 3, WINDOWHEIGHT / 2.5)
moreButton = Button(WINDOWWIDTH / 2, WINDOWHEIGHT / 1.75, WINDOWHEIGHT / 5)
lessButton = Button(WINDOWWIDTH / 2, WINDOWHEIGHT / 1.33, WINDOWHEIGHT / 5)
startButton = Button(WINDOWWIDTH / 2, WINDOWHEIGHT / 1.15, WINDOWHEIGHT / 2.5)
menuButton = Button(WINDOWWIDTH / 1.17, WINDOWHEIGHT / 1.1, WINDOWHEIGHT / 7)
quitButton = Button(WINDOWWIDTH / 1.055, WINDOWHEIGHT / 1.1, WINDOWHEIGHT / 7)
pauseButton = Button(WINDOWWIDTH / 1.34, WINDOWHEIGHT / 1.1, WINDOWHEIGHT / 5)
initButton = Button(WINDOWWIDTH / 1.34, WINDOWHEIGHT / 1.1, WINDOWHEIGHT / 5)


startMenuSprites = pygame.sprite.Group()
startMenuSprites.add(bubbleButton, insertionButton, selectionButton, bogoButton, mergeButton, quickButton, moreButton, lessButton, startButton)
sortingSprites = pygame.sprite.Group()
sortingSprites.add(menuButton)
quitSprites = pygame.sprite.Group()
quitSprites.add(quitButton)
pauseSprites = pygame.sprite.Group()
pauseSprites.add(pauseButton)
initiateSprites = pygame.sprite.Group()
initiateSprites.add(initButton)

while True:
    DISPLAYSURF.fill(BLACK)
    
    MouseXY = pygame.mouse.get_pos()
    Mouse.update(MouseXY[0], MouseXY[1])

    if programMode == 0:
        startMenuSprites.draw(DISPLAYSURF)
        
        if pygame.sprite.collide_rect(Mouse, insertionButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'insertion'
        elif pygame.sprite.collide_rect(Mouse, bubbleButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'bubble'
        elif pygame.sprite.collide_rect(Mouse, selectionButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'selection'
        elif pygame.sprite.collide_rect(Mouse, bogoButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'bogo'
        elif pygame.sprite.collide_rect(Mouse, mergeButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'merge'
        elif pygame.sprite.collide_rect(Mouse, quickButton) and event.type == pygame.MOUSEBUTTONDOWN:
            selected = 'quick'
        
        if moreButton.update(False, 'MORE') and bars < 1000:
            bars += 1
        if lessButton.update(False, 'LESS') and bars > 2:
            bars -= 1
        if startButton.update(False, 'START') and selected != '':
            programMode = 1
            #generate bars
            nums = []
            for i in range(1, bars+1):
                nums.append([])
                nums[i-1].append(i)
            random.shuffle(nums)
            region = WINDOWHEIGHT / 6 / 1.5

            #data calculation
            for i in range(len(nums)):
                nums[i].append((WINDOWHEIGHT / 1.5 / bars) * nums[i][0])
                if nums[i][1] >= region * 5 and nums[i][1] <= region * 6:
                    nums[i].append(244)
                    nums[i].append(66)
                    nums[i].append(int((((region - (nums[i][1] - (region * 5))) / region) * 178) + 66))
                elif nums[i][1] >= region * 4 and nums[i][1] < region * 5:
                    nums[i].append(int((((nums[i][1] - (region * 4)) / region) * 178) + 66))
                    nums[i].append(66)
                    nums[i].append(244)
                elif nums[i][1] >= region * 3 and nums[i][1] < region * 4:
                    nums[i].append(66)
                    nums[i].append(int(((((region - (nums[i][1] - (region * 3)))) / region) * 178) + 66))
                    nums[i].append(244)
                elif nums[i][1] >= region * 2 and nums[i][1] < region * 3:
                    nums[i].append(66)
                    nums[i].append(244)
                    nums[i].append(int((((nums[i][1] - (region * 2)) / region) * 178) + 66))
                elif nums[i][1] >= region and nums[i][1] < region * 2:
                    nums[i].append(int((((region - (nums[i][1] - (region))) / region) * 178) + 66))
                    nums[i].append(244)
                    nums[i].append(66)
                elif nums[i][1] >= 0 and nums[i][1] < region:
                    nums[i].append(244)
                    nums[i].append(int(((nums[i][1] / region) * 178) + 66))
                    nums[i].append(66)

            current = nums[1]
            barGap = WINDOWWIDTH / 1.3 / bars
            startPosX = WINDOWWIDTH / 8
            startPosY = WINDOWHEIGHT / 1.2

        drawText(DISPLAYSURF, str(bars), int(WINDOWHEIGHT / 20), int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 1.5), RED, 'calibri', 'mt')

        if selected == 'insertion':
            insertionButton.update(True, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(False, 'QUICK')
        elif selected == 'selection':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(True, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(False, 'QUICK')
        elif selected == 'bubble':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(True, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(False, 'QUICK')
        elif selected == 'bogo':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(True, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(False, 'QUICK')
        elif selected == 'merge':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(True, 'MERGE')
            quickButton.update(False, 'QUICK')
        elif selected == 'quick':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(True, 'QUICK')
        elif selected == '':
            insertionButton.update(False, 'INSERTION')
            bubbleButton.update(False, 'BUBBLE')
            selectionButton.update(False, 'SELECTION')
            bogoButton.update(False, 'BOGO')
            mergeButton.update(False, 'MERGE')
            quickButton.update(False, 'QUICK')
        
        drawText(DISPLAYSURF, 'SORTER', int(WINDOWHEIGHT / 10.5), int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 10), RED, 'calibri', 'c')
        drawText(DISPLAYSURF, 'PICK A SORTING METHOD', int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 6), RED, 'calibri', 'c')
        drawText(DISPLAYSURF, 'HOW MANY BARS', int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2), RED, 'calibri', 'c')

    elif programMode == 1:
        sortingSprites.draw(DISPLAYSURF)
        for i in range(len(nums)):
            pygame.draw.line(DISPLAYSURF, (nums[i][2], nums[i][3], nums[i][4]), (int(startPosX + barGap * i), int(startPosY)), (int(startPosX + barGap * i), int(startPosY - nums[i][1])), int(barGap - 2))

        #sorting
        if not init and not complete:
            initiateSprites.draw(DISPLAYSURF)
            if initButton.update(False, 'INITIATE') and buffer == 0:
                init = not init
                buffer = 40
                
        elif init and not complete:
            if selected == 'bubble':
                
                if nums[count][0] > nums[count + 1][0]:
                    temp = nums[count]
                    nums[count] = nums[count + 1]
                    nums[count + 1] = temp
                    swap = True
                comps += 1
                count += 1
                
                if count == len(nums)-passes-1:
                    passes += 1
                    if swap == False:
                        complete = True
                        init = False
                    swap = False
                    count = 0
                
            elif selected == 'insertion':

                if count+1 == len(nums):
                    init = False
                    complete = True
                if not complete:
                    if nums[pos] == current:
                        count += 1
                        current = nums[count]
                        pos = count
                    if pos > 0 and nums[pos-1][0] > current[0]:
                        nums[pos] = nums[pos-1]
                        pos -= 1
                        comps += 1
                    else:
                        nums[pos] = current

            elif selected == 'selection':
                   
                if count < len(nums):
                    if nums[minPos][0] > nums[count][0]:
                        minPos = count
                    count += 1
                    comps += 1
                elif count >= len(nums):
                    temp = nums[passes]
                    nums[passes] = nums[minPos]
                    nums[minPos] = temp
                    passes += 1
                    minPos = passes
                    count = minPos + 1
                    if passes == len(nums):
                        complete = True

            elif selected == 'bogo':

                outOfOrder = False
                random.shuffle(nums)
                for i in range(len(nums)-1):
                    if nums[i][0] > nums[i+1][0]:
                        outOfOrder = True
                if outOfOrder == False:
                    complete = True

            elif selected == "merge":
                pass

            elif selected == "quick":
                pass
                    
            
            pauseSprites.draw(DISPLAYSURF)
            if pauseButton.update(False, 'PAUSE') and buffer == 0:
                init = not init
                buffer = 40

        elif complete:
            drawText(DISPLAYSURF, 'COMPLETE', int(WINDOWHEIGHT / 20), int(WINDOWWIDTH / 1.34), int(WINDOWHEIGHT / 1.1 + WINDOWHEIGHT / 30), RED, 'calibri', 'c')
            pygame.draw.lines(DISPLAYSURF, RED, True, ((int(WINDOWWIDTH / 1.34 - moveX),int(WINDOWHEIGHT / 1.1 - moveY + WINDOWHEIGHT / 30)), (int(WINDOWWIDTH / 1.34 + moveX),int(WINDOWHEIGHT / 1.1 - moveY + WINDOWHEIGHT / 30)),
                                                (int(WINDOWWIDTH / 1.34 + moveX),int(WINDOWHEIGHT / 1.1 + moveY + WINDOWHEIGHT / 30)), (int(WINDOWWIDTH / 1.34 - moveX),int(WINDOWHEIGHT / 1.1 + moveY + WINDOWHEIGHT / 30))), int(WINDOWWIDTH / 360))

        #menu button
        if menuButton.update(False, 'MENU'):
            programMode = 0
            complete = False
            count = 0
            passes = 0
            comps = 0
            init = False
            pos = 0

        #counter
        drawText(DISPLAYSURF, 'COMPARISONS:', int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 11), int(WINDOWHEIGHT / 20), RED, 'calibri', 'c')
        if comps >= 0 and comps <= 99:
            drawText(DISPLAYSURF, str(comps), int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 5.8), int(WINDOWHEIGHT / 20), RED, 'calibri', 'c')
        elif comps >= 100 and comps <= 999:
            drawText(DISPLAYSURF, str(comps), int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 5.5), int(WINDOWHEIGHT / 20), RED, 'calibri', 'c')
        elif comps >= 1000 and comps <= 9999:
            drawText(DISPLAYSURF, str(comps), int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 5.3), int(WINDOWHEIGHT / 20), RED, 'calibri', 'c')
        elif comps >= 10000:
            drawText(DISPLAYSURF, str(comps), int(WINDOWHEIGHT / 25), int(WINDOWWIDTH / 5.1), int(WINDOWHEIGHT / 20), RED, 'calibri', 'c')
        
    if buffer > 0:
        buffer -= 1
        
    #Quit button
    quitSprites.draw(DISPLAYSURF)
    if quitButton.update(False, 'QUIT'):
        pygame.quit()

    pygame.draw.lines(DISPLAYSURF, RED, True, ((0,0), (WINDOWWIDTH,0), (WINDOWWIDTH,WINDOWHEIGHT), (0,WINDOWHEIGHT)), 20)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
