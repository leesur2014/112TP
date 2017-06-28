################################################################################ 
##Video link: https://youtu.be/pDEpEhmmN88 
################################################################################ 
## CITATION
################################################################################
# PYGAMEGAME is from Lukas Peraza
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py
################################################################################
# all PICTURES cite from http://tieba.baidu.com/p/4340270718?pn=1
################################################################################
# for ANIMATION, the updateImage method cites from Lukas Peraza 
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Explosion.py
################################################################################
# for FILE R&W, cite from 15112 course website
# http://www.kosbie.net/cmu/fall-14/15-112/notes/file-and-web-io.py
################################################################################

from __future__ import with_statement # for Python 2.5 and 2.6
import contextlib # for urllib.urlopen()
import urllib
import os

import pygame
from pygamegame import PygameGame
import math
import random
import copy

################################################################################ 
## Gunner Class
################################################################################
class Gunner(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.angle = 0
        self.image = pygame.transform.rotate(pygame.transform.scale(
                     pygame.image.load('gunner.png'),(150, 150)), self.angle)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        pass

################################################################################ 
## Bullet Class
################################################################################
class Bullet(pygame.sprite.Sprite):
    imageSize = (40, 40)
    centerx = 115
    centery = 515
    velocity = 30

    def __init__(self, x, y):        
        self.angle = 0
        self.radious = 50
        self.angleSpd = math.pi / 180
        self.minAngle = - math.pi / 2
        self.maxAngle = 0       
        self.image = pygame.transform.scale(pygame.image.load('bullet.png'),
                                            Bullet.imageSize)
        self.splitImage = pygame.transform.scale(pygame.image.load('split.png'),
                                            Bullet.imageSize)
        self.g = 1 
        self.x, self.y = x, y 
        self.vx = Bullet.velocity * math.sin(self.angle)
        self.vy = -Bullet.velocity * math.cos(self.angle)        
        self.state = 1
        self.flying = False
        self.bounce = False
        
        self.secondx = x + 50
        self.secondy = y + 50       
        self.secondvx = Bullet.velocity * math.sin(self.angle)
        self.secondvy = -Bullet.velocity * math.cos(self.angle)
        self.secondState = 1
        self.secondFlying = False
        self.secondBounce = False
        
        self.frame = 0
        self.frameRate = 23
        self.aliveTime = 0

        self.w = 0
        self.updateImage()

    def draw(self, screen):
        screen.blit(self.image, (10, 10))
        endx = Bullet.centerx + self.radious * math.cos(self.angle)
        endy = Bullet.centery + self.radious * math.sin(self.angle)
        if (self.flying == False):
            self.x, self.y = endx - 20, endy - 20
            screen.blit(self.image, (endx - 20, endy - 20))
        else:
            screen.blit(self.image, (self.x, self.y))
            screen.blit(self.splitImage, (self.x, self.y))
        pygame.draw.line(screen, (0,255,0),(Bullet.centerx, Bullet.centery), 
            (endx, endy))
   
    def playInit(self):
        endx = Bullet.centerx + self.radious * math.cos(self.angle)
        endy = Bullet.centery + self.radious * math.sin(self.angle)
        self.x, self.y = endx, endy
        self.secondx, self.secondy = endx, endy

    @staticmethod
    def animation():
        size = (2 * Bullet.imageSize[0], Bullet.imageSize[1])
        image = pygame.transform.scale(pygame.image.load('fire_bullet.png'), 
                                       size)
        rows, cols = 1, 2
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Bullet.images = []
        for i in range(rows):
            for j in range(cols):
                subImage = image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Bullet.images.append(subImage)

    def updateImage(self):
        self.fireImage = Bullet.images[self.frame]
        w, h = self.fireImage.get_size()

    def drawSecondBullet(self, screen):
        endx = Bullet.centerx + self.radious * math.cos(self.angle)
        endy = Bullet.centery + self.radious * math.sin(self.angle)
        if (self.flying == False):
            self.secondx, self.secondy = endx - 20, endy - 20
            screen.blit(self.fireImage, (endx - 20, endy - 20))
        else:
            screen.blit(self.fireImage, (self.secondx, self.secondy))

    def update(self, keysDown, screenWidth, screenHeight):
        self.angle += self.angleSpd
        if (self.angle < self.minAngle or self.angle > self.maxAngle):
            self.angleSpd = - self.angleSpd
        if (self.state == 1 and self.flying == True):
            self.vy += self.g
            self.x += self.vx 
            self.y += self.vy
            if (self.x < 0 or self.x > screenWidth or self.y < 0 or 
                self.y > screenHeight):
                self.state = 0
                self.flying = False
                self.bounce = False
        else:
            endx = Bullet.centerx + self.radious * math.cos(self.angle)
            endy = Bullet.centery + self.radious * math.sin(self.angle)
            self.x, self.y = endx - 20, endy - 20
            if (keysDown(pygame.K_SPACE)):
                #print("space")
                self.flying = True
                self.bounce = False
                self.state = 1
                self.vy = -Bullet.velocity * math.sin(-self.angle)
                self.vx = Bullet.velocity * math.cos(-self.angle)

    def bullet3Update(self, keyDown, screenWidth, screenHeight):
        self.angle += self.angleSpd
        self.windSpd = 5
        if (self.angle < self.minAngle or self.angle > self.maxAngle):
            self.angleSpd = - self.angleSpd
        if (self.state == 1 and self.flying == True):
            self.vy += self.g
            self.x += self.vx 
            self.y += self.vy
            if (self.x < 0 or self.x > screenWidth or self.y < 0 or 
                self.y > screenHeight):
                self.state = 0
                self.flying = False
        else:
            endx = Bullet.centerx + self.radious * math.cos(self.angle)
            endy = Bullet.centery + self.radious * math.sin(self.angle)
            self.x, self.y = endx - 20, endy - 20
            if ((not keyDown) and self.w > 0):
                self.flying = True
                self.bounce = False
                self.state = 1               
                self.vy = -Bullet.velocity*2*math.sin(-self.angle) * self.w / 80
                self.vx = (Bullet.velocity*2*math.cos(-self.angle) * self.w / 80
                           - self.windSpd)
                self.w = 0

    def updateSecond(self, dt, keysDown, screenWidth, screenHeight):
        self.aliveTime += dt
        self.frame = self.aliveTime % (1000 % self.frameRate)
        if (self.frame < len(Bullet.images)):
            self.updateImage()
        if (self.secondState == 1 and self.secondFlying == True):
            self.secondvy += self.g
            self.secondx += 2 * self.secondvx 
            self.secondy += self.secondvy
            if (self.secondx < 0 or self.secondx > screenWidth or 
                self.secondy < 0 or self.secondy > screenHeight):
                self.secondState = 0
                self.secondFlying = False
                self.secondBounce = False
        else:
            endx = Bullet.centerx + self.radious * math.cos(self.angle)
            endy = Bullet.centery + self.radious * math.sin(self.angle)
            self.secondx, self.secondy = endx - 20, endy - 20
            if (keysDown(pygame.K_SPACE)): 
                self.secondFlying = True
                self.secondBounce = False
                self.secondState = 1
                self.secondvy = -Bullet.velocity * math.sin(-self.angle)
                self.secondvx = Bullet.velocity * math.cos(-self.angle)

    def launch(self, keyDown):
        self.engyAddSpd = 3
        if (keyDown):
            self.w += self.engyAddSpd
        if (self.w > 80):
            self.w = 0

    def drawEngyBar(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (20, 400, 80, 20), 3)
        pygame.draw.rect(screen, (255, 0, 0), (20, 400, self.w, 20))

################################################################################ 
## Target Class
################################################################################             
class Target(object):
    imageSize = (120, 140)
    potSize = (80, 100)
    minPosition = 300
    maxPosition = 600
    imageNumber = 3

    @staticmethod
    def init():
        Target.pot_image = pygame.transform.scale(pygame.image.load(
                       'pot.png'),Target.potSize)
        Target.potPositionList = [[Target.minPosition, Target.minPosition * 0.5],
                        [Target.maxPosition * 0.8, Target.minPosition], 
                        [Target.maxPosition  , Target.minPosition * 0.5]]
        size1 = (Target.imageSize[0] * 4, Target.imageSize[1] * 3)
        zombie1_image = pygame.transform.scale(pygame.image.load('zombie1.png'), 
                                       size1)
        zombie1_rows, zombie1_cols = 3, 4
        width, height = zombie1_image.get_size()
        cellWidth, cellHeight = width / zombie1_cols, height / zombie1_rows
        Target.zombie1_images = []
        for i in range(zombie1_rows):
            for j in range(zombie1_cols):
                subImage = zombie1_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Target.zombie1_images.append(subImage)

        size2 = (Target.imageSize[0] * 5, Target.imageSize[1] * 3)
        zombie2_image = pygame.transform.scale(pygame.image.load('zombie2.png'), 
                                       size2)
        zombie2_rows, zombie2_cols = 3, 5
        width, height = zombie2_image.get_size()
        cellWidth, cellHeight = width / zombie2_cols, height / zombie2_rows
        Target.zombie2_images = []
        for i in range(zombie2_rows):
            for j in range(zombie2_cols):
                subImage = zombie2_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Target.zombie2_images.append(subImage)

        size3 = (Target.imageSize[0] * 4, Target.imageSize[1] * 3)
        zombie3_image = pygame.transform.scale(pygame.image.load('zombie3.png'), 
                                       size3)
        zombie3_rows, zombie3_cols = 3, 4
        width, height = zombie3_image.get_size()
        cellWidth, cellHeight = width / zombie3_cols, height / zombie3_rows
        Target.zombie3_images = []
        for i in range(zombie3_rows):
            for j in range(zombie3_cols):
                subImage = zombie3_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Target.zombie3_images.append(subImage)

        size3 = (Target.imageSize[0] * 4, Target.imageSize[1] * 3)
        zombieDie_image = pygame.transform.scale(pygame.image.load('boomDie.png'), 
                                       size3)
        zombieDie_rows, zombieDie_cols = 3, 4
        width, height = zombieDie_image.get_size()
        cellWidth, cellHeight = width / zombieDie_cols, height / zombieDie_rows
        Target.zombieDie_images = []
        for i in range(zombieDie_rows):
            for j in range(zombieDie_cols):
                subImage = zombieDie_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Target.zombieDie_images.append(subImage)

    def __init__(self):
        self.alpha = 255
        self.state = [1, 1, 1]
        #self.state = [0, 1, 0]
        self.positionList = Target.potPositionList
        self.clock = [12, 12, 12]
        self.frequency = 1 
        self.frame = 0
        self.frameRate = 17
        self.aliveTime = 10

        self.updateImage()
        self.updateImage2()

    def updateImage(self):
        self.zombie1Image = Target.zombie1_images[self.frame]
        self.zombie3Image = Target.zombie3_images[self.frame]
        self.zombieDieImage = Target.zombieDie_images[self.frame]

    def updateImage2(self):
        self.zombie2Image = Target.zombie2_images[self.frame]

    def updateZombie(self, dt):
        self.aliveTime += dt
        self.frame = self.aliveTime % (self.frameRate)
        if (self.frame < len(Target.zombie1_images)):
            self.updateImage()
        if (self.frame < len(Target.zombie2_images)):
            self.updateImage2()

    def playInit(self):
        self.state = [1, 1, 1]
        #self.state = [0, 1, 0] #for testing
        self.clock = [12, 12, 12]

    def draw(self, screen):
        for i in range(3):
            screen.blit(Target.pot_image, 
                (self.positionList[i][0] + Target.imageSize[0] * 0.3,
                 self.positionList[i][1] + Target.imageSize[1] * 0.6))
        if (self.state[0] > 0):            
            screen.blit(self.zombie2Image, self.positionList[0])
        if (self.state[1] > 0):            
            screen.blit(self.zombie1Image, self.positionList[1])
        if (self.state[2] > 0):            
            screen.blit(self.zombie3Image, self.positionList[2])
        for i in range(3):
            if (self.state[i] == 0 and self.clock[i] > 0):
                screen.blit(self.zombieDieImage, self.positionList[i])

    def update(self):
        for i in range(3):
            if (self.state[i] == 0):
                self.clock[i] -= self.frequency
                if (self.clock[i] < 0):
                    self.clock[i] = 0

    def collisionTest(self, otherx, othery, otherState):
        xoffset = 20
        for i in range(Target.imageNumber):
            (x1, y1, x2, y2) = (self.positionList[i][0] + xoffset,
                        self.positionList[i][1], 
                        self.positionList[i][0] + Target.imageSize[0] + xoffset, 
                        self.positionList[i][1] + Target.imageSize[1])
            if (otherx > x1 and otherx < x2 and othery > y1 and othery < y2 and 
                self.state[i] > 0 and otherState == 1):
                self.state[i] -= 1
                otherState = 0
                return True
        return False

################################################################################ 
## Obstacle Class
################################################################################
class Obstacle(object): 
    imageSize = (80, 100)
    staticSize = (70, 110)
    minPosition = 300
    maxPosition = 600
    imageNumber = 4
    putRect = [[150, 80], [250, 80], [350, 80], [450, 80]]
    
    @staticmethod
    def init():
        size = (Obstacle.imageSize[0] * 4, Obstacle.imageSize[1])
        blower_image = pygame.transform.scale(pygame.image.load('blower.png'), 
                                       size)
        blower_rows, blower_cols = 1, 4
        width, height = blower_image.get_size()
        cellWidth, cellHeight = width / blower_cols, height / blower_rows
        Obstacle.blower_images = []
        for i in range(blower_rows):
            for j in range(blower_cols):
                subImage = blower_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Obstacle.blower_images.append(subImage)
        n_size = (Obstacle.imageSize[0] * 7, Obstacle.imageSize[0] * 3)
        nut_image = pygame.transform.scale(pygame.image.load('nuts.png'), 
                                       n_size)
        nut_rows, nut_cols = 2, 7
        width, height = nut_image.get_size()
        cellWidth, cellHeight = width / nut_cols, height / nut_rows
        Obstacle.nut_images = []
        for i in range(nut_rows):
            for j in range(nut_cols):
                subImage = nut_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Obstacle.nut_images.append(subImage)

    def __init__(self, image):
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            Obstacle.staticSize)
        self.frame1 = 0
        self.frame2 = 0
        self.frameRate = 17
        self.aliveTime = 10
        self.dragx, self.dragy = 0, 0
        self.putRect = copy.deepcopy(Obstacle.putRect)
        self.posList = []

        self.updateImage()

    def playInit(self):
        self.posList = []
        self.putRect = copy.deepcopy(Obstacle.putRect)

    def updateImage(self):
        self.blowerImage = Obstacle.blower_images[self.frame1]

    def updateNutImage(self):
        self.nutImage = Obstacle.nut_images[self.frame2]
           
    def updateBlower(self, dt):
        self.aliveTime += dt
        self.frame1 = self.aliveTime % (self.frameRate)
        if (self.frame1 < len(Obstacle.blower_images)):
            self.updateImage()
    
    def updateNut(self, dt):
        self.aliveTime += dt
        self.frame2 = self.aliveTime % (self.frameRate)
        if (self.frame2 < len(Obstacle.nut_images)):
            self.updateNutImage()

    def drawBlower(self, screen):
        pos = (450, 165)
        for i in range(4):           
            screen.blit(self.blowerImage, (pos[0], i * pos[1]))

    def draw(self, screen):
        for rect in self.posList:
            screen.blit(self.nutImage, rect)

    def drawPut(self, screen, put, drag): 
        if (put):
            for rect in self.putRect:
                screen.blit(self.image, rect)      
            if (drag):
                screen.blit(self.image, (self.dragx - Obstacle.imageSize[0] * 0.25, 
                        self.dragy - Obstacle.imageSize[1] * 0.25))

    def bounceTest(self, otherx, othery, otherr, otherState):
        #otherx, othery are center coordinate of bullet
        offset2 = 10
        for leftTop in self.posList:
            (x1, y1, x2, y2) = (leftTop[0], leftTop[1] - 2 * offset2, 
                leftTop[0] + Obstacle.imageSize[0] - offset2,
                leftTop[1] + Obstacle.imageSize[1] - offset2)  
            #print("x1,y1,x2,y2",x1, y1, x2, y2)
            #print("bx,by",otherx, othery)     
            if (otherx + otherr > x1 and otherx - otherr < x1 and othery > y1 
                and othery < y2 and otherState == 1):
                return 1
            elif (otherx + otherr > x2 and otherx - otherr < x2 and othery > y1 
                and othery < y2 and otherState == 1):
                return 1
            elif (otherx - 20 > x1 and otherx < x2 and othery + 2 * offset2 > y1 and 
                othery < y1 and otherState == 1):
                return 2
            elif (otherx + 10 > x1 and otherx + 10 < x2 and othery > y2 + offset2 and 
                  othery < y2 + offset2 and otherState == 1):
                return 2
        return 0 

################################################################################ 
## Menu Class
################################################################################
class Menu(object):
    imageSize = (800, 600)
    smallImageSize = (400, 300)
    lawnSize = (500, 60)
    longLawnSize = (820, 90)
    scoreLawnSize = (100, 40)
    bestScoreSize = (200, 60)
    levelSize = (180, 150)
    levelPosition = (310, 0)
    buttonSize = (120, 60)
    buttonRect = ((200, 400), (450, 400), (650, 0), (300, 400), (650, 530),
                  (200,200), (20, 20), (650, 60), (100,150), (650,480), 
                  (325, 400))
# buttonRect=((200,400) #play,(450,400),(650,0)#help,(300,400)#next(650,530)#pause,
#(200,200))#continue,(20, 20)#back,(650,60)#put,(100,150)#lawn,
#(650,480)#backtohome, (325, 400)#backtogame)

    @staticmethod
    def scoreInit():
        Menu.score_image = pygame.image.load('score.png')
        rows, cols = 2, 5
        width, height = Menu.score_image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Menu.score_images = []
        for i in range(rows):
            for j in range(cols):
                subImage = Menu.score_image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Menu.score_images.append(subImage)

    @staticmethod
    def PicInit():
        Menu.button_play_image = pygame.transform.scale(
                          pygame.image.load('button_play.png'), Menu.buttonSize)
        Menu.button_help_image = pygame.transform.scale(
                          pygame.image.load('button_help.png'), Menu.buttonSize)
        Menu.button_back_image = pygame.transform.scale(
                          pygame.image.load('button_back.png'), Menu.buttonSize)
        Menu.button_pause_image = pygame.transform.scale(
                          pygame.image.load('button_pause.png'), Menu.buttonSize)
        Menu.button_put_image = pygame.transform.scale(
                          pygame.image.load('button_put.png'), Menu.buttonSize)
        Menu.continue_image = pygame.transform.scale(
                        pygame.image.load('continue.jpg'), Menu.smallImageSize)
        Menu.lawn_image = pygame.transform.scale(
                        pygame.image.load('lawn.png'), Menu.lawnSize)
        Menu.longLawn_image = pygame.transform.scale(
                        pygame.image.load('lawn.png'), Menu.longLawnSize)
        Menu.scoreLawn_image = pygame.transform.scale(
                        pygame.image.load('lawn.png'), Menu.scoreLawnSize)
        Menu.reminder_image = pygame.transform.scale(
                        pygame.image.load('reminder.png'), Menu.smallImageSize)
        Menu.instruction_image = pygame.transform.scale(
                        pygame.image.load('instruction1.png'), Menu.smallImageSize)
        Menu.level1_image = pygame.transform.scale(
                          pygame.image.load('level1.png'), Menu.levelSize)
        Menu.level2_image = pygame.transform.scale(
                          pygame.image.load('level2.png'), Menu.levelSize)
        Menu.level3_image = pygame.transform.scale(
                          pygame.image.load('level3.png'), Menu.levelSize)
        Menu.eaten_image = pygame.transform.scale(
                            pygame.image.load('eaten.png'),(300, 300))
        Menu.button_play_again = pygame.transform.scale(
                        pygame.image.load('play_again.png'), Menu.buttonSize)
        Menu.win_image = pygame.transform.scale(
                            pygame.image.load('winner.png'),(550, 200))
        Menu.button_next = pygame.transform.scale(
                        pygame.image.load('next.png'), Menu.buttonSize)
        Menu.button_restart = pygame.transform.scale(
                        pygame.image.load('restart.png'), (150, 70))
        Menu.bestScore_image = pygame.transform.scale(
                        pygame.image.load('bestScore.png'), Menu.bestScoreSize)
        
    def __init__(self, x, y, image):       
        self.x, self.y = x, y
        self.life = 6
        self.image = pygame.transform.scale(pygame.image.load(
                                image), Menu.imageSize)
    def playInit(self):
        self.life = 6

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def drawLongLawn(self, screen):
        screen.blit(Menu.longLawn_image, (-10, 519))

    def drawLevel(self, screen, level):
        if (level == 1):
            screen.blit(Menu.level1_image, Menu.levelPosition)
        elif (level == 2):
            screen.blit(Menu.level2_image, Menu.levelPosition)
        else:
            screen.blit(Menu.level3_image, Menu.levelPosition)

    def drawScore(self, screen, score):
        image = Menu.score_images[self.life - 1]
        factor = 1
        w, h = image.get_size()
        scoreImage = pygame.transform.scale(image, (int(w * factor), 
                                               int(h * factor)))
        screen.blit(scoreImage, (50, 0))
        screen.blit(Menu.scoreLawn_image, (0, 50))
        score = str(score)
        for i in range(len(score)):
            num = int(score[i])
            score_subImage = Menu.score_images[num - 1]
            smallScoreImage = pygame.transform.scale(score_subImage, 
                                (25, 25))
            screen.blit(smallScoreImage, ( i * 20, 60))       

    def drawButton(self, screen, score): 
        screen.blit(self.image, (self.x, self.y))
        screen.blit(Menu.button_play_image, Menu.buttonRect[0])
        screen.blit(Menu.button_help_image, Menu.buttonRect[1])
        screen.blit(Menu.bestScore_image, (300, 500))
        score = str(score)
        for i in range(len(score)):
            num = int(score[i])
            score_subImage = Menu.score_images[num - 1]
            smallScoreImage = pygame.transform.scale(score_subImage, 
                                (30, 30))
            screen.blit(smallScoreImage, ( 415 + i * 20, 515))


    def drawBackToGame(self, screen):
        screen.blit(Menu.button_back_image, Menu.buttonRect[10])

    def drawButtonHelp(self, screen):
        screen.blit(Menu.button_help_image, Menu.buttonRect[2])
        screen.blit(Menu.button_pause_image, Menu.buttonRect[4])
        screen.blit(Menu.button_put_image, Menu.buttonRect[7])
        screen.blit(Menu.button_back_image, Menu.buttonRect[9])

# buttonRect=((200,400) #play,(450,400),(650,0)#help,(300,400)#next(650,530)#pause,
#(200,200))#continue,(20, 20)#back,(650,60)#put,(100,150)#lawn)
    def drawBack(self, screen):
        screen.blit(Menu.instruction_image, Menu.buttonRect[5])
        screen.blit(Menu.button_back_image, Menu.buttonRect[6])

    def drawPause(self, screen, pause, put):
        if (pause and not put):
            screen.blit(Menu.continue_image, Menu.buttonRect[5])

    def drawPut(self, screen, put):
        if put:
            screen.blit(Menu.lawn_image, Menu.buttonRect[8])

    def drawReminder(self, screen, start):
        if (not start):
            screen.blit(Menu.reminder_image, Menu.buttonRect[5])

    def drawLose(self, screen):
        screen.blit(Menu.eaten_image, (250, 0))
        screen.blit(Menu.button_play_again, Menu.buttonRect[3])
        screen.blit(Menu.button_help_image, Menu.buttonRect[2])

    def drawWin(self, screen):
        screen.blit(Menu.win_image, (120, 100))
        screen.blit(Menu.button_next, Menu.buttonRect[3])
        screen.blit(Menu.button_help_image, Menu.buttonRect[2])

    def drawEnd(self, screen):
        screen.blit(Menu.win_image, (120, 100))
        screen.blit(Menu.button_restart, Menu.buttonRect[3])
        screen.blit(Menu.button_help_image, Menu.buttonRect[2])

################################################################################
def homeMousePressed(self, x, y):
    p_w = (Menu.buttonRect[0][0], Menu.buttonRect[0][0] + Menu.buttonSize[0])
    p_h = (Menu.buttonRect[0][1], Menu.buttonRect[0][1] + Menu.buttonSize[1])
    if (x in range(p_w[0], p_w[1]) and y in range(p_h[0], p_h[1])):
        self.mode = "levelOnePlay"
    h_w = (Menu.buttonRect[1][0], Menu.buttonRect[1][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[1][1], Menu.buttonRect[1][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "home"
    #back to game 
    b_w = (Menu.buttonRect[10][0], Menu.buttonRect[10][0] + Menu.buttonSize[0])
    b_h = (Menu.buttonRect[10][1], Menu.buttonRect[10][1] + Menu.buttonSize[1])
    if (x in range(b_w[0], b_w[1]) and y in range(b_h[0], b_h[1])):
        self.mode = self.lastMode
        self.backToHome = False 

def helpMousePressed(self, x, y):
    h_w = (Menu.buttonRect[6][0], Menu.buttonRect[6][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[6][1], Menu.buttonRect[6][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = self.lastMode

def levelOnePlayMousePressed(self, x, y):
    if (self.start):
        #help
        h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
        h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
        if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
            self.mode = "help"
            self.lastMode = "levelOnePlay"
        #pause
        p_w = (Menu.buttonRect[4][0], Menu.buttonRect[4][0] + Menu.buttonSize[0])
        p_h = (Menu.buttonRect[4][1], Menu.buttonRect[4][1] + Menu.buttonSize[1])
        if (x in range(p_w[0], p_w[1]) and y in range(p_h[0], p_h[1])):
            pygame.mixer.music.pause()
            self.pause = True 
        #back to home 
        b_w = (Menu.buttonRect[9][0], Menu.buttonRect[9][0] + Menu.buttonSize[0])
        b_h = (Menu.buttonRect[9][1], Menu.buttonRect[9][1] + Menu.buttonSize[1])
        if (x in range(b_w[0], b_w[1]) and y in range(b_h[0], b_h[1])):
            self.mode = "home"
            self.lastMode = "levelOnePlay"
            self.backToHome = True    
        #continue
        c_w = (Menu.buttonRect[5][0], Menu.buttonRect[5][0] + Menu.smallImageSize[0])
        c_h = (Menu.buttonRect[5][1], Menu.buttonRect[5][1] + Menu.smallImageSize[1])
        if (x in range(c_w[0], c_w[1]) and y in range(c_h[0], c_h[1])):
            self.pause = False
        #put obstacle 
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1]) and 
            self.alreadyPut == False):
            self.pause = True
            self.put = True
            self.alreadyPut = True
    else:
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1])):
            self.start = True

    
def levelOneLoseMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelOneLose"
    ag_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    ag_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(ag_w[0], ag_w[1]) and y in range(ag_h[0], ag_h[1])):              
        self.alreadyPut = False
        self.obstacle.playInit()
        self.menu.playInit()
        self.target.playInit()
        self.bullet.playInit()
        self.start = False
        self.mode = "levelOnePlay"

def levelOneWinMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelOneWin"
    n_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    n_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(n_w[0], n_w[1]) and y in range(n_h[0], n_h[1])):
        self.mode = "levelTwoPlay"
        self.alreadyPut = False
        self.start = False
        self.menu2.playInit()
        self.target2.playInit()
        self.bullet2.playInit()

def levelTwoPlayMousePressed(self, x, y):
    if (self.start):
        h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
        h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
        if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
            self.mode = "help"
            self.lastMode = "levelTwoPlay"
        p_w = (Menu.buttonRect[4][0], Menu.buttonRect[4][0] + Menu.buttonSize[0])
        p_h = (Menu.buttonRect[4][1], Menu.buttonRect[4][1] + Menu.buttonSize[1])
        if (x in range(p_w[0], p_w[1]) and y in range(p_h[0], p_h[1])):
            pygame.mixer.music.pause()
            self.pause = True
        c_w = (Menu.buttonRect[5][0], Menu.buttonRect[5][0] + Menu.smallImageSize[0])
        c_h = (Menu.buttonRect[5][1], Menu.buttonRect[5][1] + Menu.smallImageSize[1])
        if (x in range(c_w[0], c_w[1]) and y in range(c_h[0], c_h[1])):
            self.pause = False
        #back to home &&
        b_w = (Menu.buttonRect[9][0], Menu.buttonRect[9][0] + Menu.buttonSize[0])
        b_h = (Menu.buttonRect[9][1], Menu.buttonRect[9][1] + Menu.buttonSize[1])
        if (x in range(b_w[0], b_w[1]) and y in range(b_h[0], b_h[1])):
            self.mode = "home"
            self.lastMode = "levelTwoPlay"
            self.backToHome = True 
        #put obstacle
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1]) and
            self.alreadyPut == False):
            self.pause = True
            self.put = True
            self.alreadyPut = True
    else:
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1])):
            self.start = True

def levelTwoLoseMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelTwoLose"
    ag_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    ag_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(ag_w[0], ag_w[1]) and y in range(ag_h[0], ag_h[1])):      
        self.alreadyPut = False
        self.obstacle2.playInit()
        self.menu2.playInit()
        self.target2.playInit()
        self.bullet2.playInit()
        self.start = False
        self.mode = "levelTwoPlay"

def levelTwoWinMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelTwoWin"
    ag_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    ag_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(ag_w[0], ag_w[1]) and y in range(ag_h[0], ag_h[1])):
        self.mode = "levelThreePlay"
        self.alreadyPut = False
        self.start = False
        self.menu3.playInit()
        self.target3.playInit()
        self.bullet3.playInit()

def levelThreePlayMousePressed(self, x, y):
    if (self.start):
        h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
        h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
        if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
            self.mode = "help"
            self.lastMode = "levelThreePlay"
        p_w = (Menu.buttonRect[4][0], Menu.buttonRect[4][0] + Menu.buttonSize[0])
        p_h = (Menu.buttonRect[4][1], Menu.buttonRect[4][1] + Menu.buttonSize[1])
        if (x in range(p_w[0], p_w[1]) and y in range(p_h[0], p_h[1])):
            pygame.mixer.music.pause()
            self.pause = True
        c_w = (Menu.buttonRect[5][0], Menu.buttonRect[5][0] + Menu.smallImageSize[0])
        c_h = (Menu.buttonRect[5][1], Menu.buttonRect[5][1] + Menu.smallImageSize[1])
        if (x in range(c_w[0], c_w[1]) and y in range(c_h[0], c_h[1])):
            self.pause = False
        #back to home &&
        b_w = (Menu.buttonRect[9][0], Menu.buttonRect[9][0] + Menu.buttonSize[0])
        b_h = (Menu.buttonRect[9][1], Menu.buttonRect[9][1] + Menu.buttonSize[1])
        if (x in range(b_w[0], b_w[1]) and y in range(b_h[0], b_h[1])):
            self.mode = "home"
            self.lastMode = "levelThreePlay"
            self.backToHome = True 
        #put obstacle
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1]) and 
            self.alreadyPut == False):
            self.pause = True
            self.put = True
            self.alreadyPut = True
    else:
        put_w = (Menu.buttonRect[7][0], Menu.buttonRect[7][0] + Menu.buttonSize[0])
        put_h = (Menu.buttonRect[7][1], Menu.buttonRect[7][1] + Menu.buttonSize[1])
        if (x in range(put_w[0], put_w[1]) and y in range(put_h[0], put_h[1])):
            self.start = True

def levelThreeLoseMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelThreeLose"
    ag_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    ag_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(ag_w[0], ag_w[1]) and y in range(ag_h[0], ag_h[1])):
        self.alreadyPut = False
        self.obstacle3.playInit()
        self.menu3.playInit()
        self.target3.playInit()
        self.bullet3.playInit()
        self.start = False
        self.mode = "levelThreePlay"

def levelThreeWinMousePressed(self, x, y):
    h_w = (Menu.buttonRect[2][0], Menu.buttonRect[2][0] + Menu.buttonSize[0])
    h_h = (Menu.buttonRect[2][1], Menu.buttonRect[2][1] + Menu.buttonSize[1])
    if (x in range(h_w[0], h_w[1]) and y in range(h_h[0], h_h[1])):
        self.mode = "help"
        self.lastMode = "levelThreeWin"
    #restart game
    ag_w = (Menu.buttonRect[3][0], Menu.buttonRect[3][0] + Menu.buttonSize[0])
    ag_h = (Menu.buttonRect[3][1], Menu.buttonRect[3][1] + Menu.buttonSize[1])
    if (x in range(ag_w[0], ag_w[1]) and y in range(ag_h[0], ag_h[1])):
        self.mode = "home"
        recordScore(self.totalScore)
        self.alreadyPut = False
        self.start = False
        self.obstacle.playInit()
        self.menu.playInit()
        self.target.playInit()

def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def recordScore(score):
    content = readFile("score.txt", mode="rt")
    new_content = content + str(score) + " "
    writeFile("score.txt", new_content, mode="wt")

def getBestScore():
    result = readFile("score.txt", mode="rt")
    print("first result",result)
    print(type(result))
    if (result == ''):
        m = 0
    else:
        result = result.split(" ")
        l = []
        print("result",result)
        print(type(result))
        for i in range(len(result) - 1):
            l += [int(result[i])]
        m = max(l)
    return m

################################################################################
def levelOnePlaymouseReleased(self, x, y): 
    if (len(self.obstacle.putRect) > 0 and self.drag == True):
        self.obstacle.putRect.pop()
    if (self.drag == True):
        self.obstacle.posList.append([x,y])
        if (len(self.obstacle.putRect) == 0 and len(self.obstacle.posList) != 0):
            self.put = False
            self.pause = False
    self.drag = False

def levelTwoPlaymouseReleased(self, x, y): 
    if (len(self.obstacle2.putRect) > 0 and self.drag == True):
        self.obstacle2.putRect.pop()
    if (self.drag == True):
        self.obstacle2.posList.append([x,y])
        if (len(self.obstacle2.putRect) == 0 and len(self.obstacle2.posList) != 0):
            self.put = False
            self.pause = False
    self.drag = False

def levelThreePlaymouseReleased(self, x, y):
    if (len(self.obstacle3.putRect) > 0 and self.drag == True):
        self.obstacle3.putRect.pop()
    if (self.drag == True):
        self.obstacle3.posList.append([x,y])
        if (len(self.obstacle3.putRect) == 0 and len(self.obstacle3.posList) != 0):
            self.put = False
            self.pause = False
    self.drag = False

################################################################################
def levelOnePlayMouseDrag(self, x, y):
    nut_w = (Obstacle.putRect[0][0], Obstacle.putRect[0][0] + Obstacle.staticSize[0])
    nut_h = (Obstacle.putRect[0][1], Obstacle.putRect[0][1] + Obstacle.staticSize[1])
    if (x in range(nut_w[0], nut_w[1]) and y in range(nut_h[0], nut_h[1])):
        self.drag = True
    self.obstacle.dragx, self.obstacle.dragy = x, y

def levelTwoPlayMouseDrag(self, x, y):
    nut_w = (Obstacle.putRect[0][0], Obstacle.putRect[0][0] + Obstacle.staticSize[0])
    nut_h = (Obstacle.putRect[0][1], Obstacle.putRect[0][1] + Obstacle.staticSize[1])
    if (x in range(nut_w[0], nut_w[1]) and y in range(nut_h[0], nut_h[1])):
        self.drag = True
    self.obstacle2.dragx, self.obstacle2.dragy = x, y

def levelThreePlayMouseDrag(self, x, y):
    nut_w = (Obstacle.putRect[0][0], Obstacle.putRect[0][0] + Obstacle.staticSize[0])
    nut_h = (Obstacle.putRect[0][1], Obstacle.putRect[0][1] + Obstacle.staticSize[1])
    if (x in range(nut_w[0], nut_w[1]) and y in range(nut_h[0], nut_h[1])):
        self.drag = True
    self.obstacle3.dragx, self.obstacle3.dragy = x, y

################################################################################ 
def homeTimerFired(self, keysDown):
    pass

def levelOnePlayTimerFired(self, keysDown):
    if (not self.pause):
        self.obstacle.updateNut(50)
        self.target.updateZombie(50)
        self.gunner.update()
        self.bullet.update(self.isKeyPressed, self.width, self.height)
        if (self.target.collisionTest(self.bullet.x + Bullet.imageSize[0] / 2, 
            self.bullet.y + Bullet.imageSize[1] / 2, self.bullet.state)):
            self.totalScore += 30
            self.bullet.state = 0
            self.menu.life -= 1
        if (self.target.collisionTest(self.bullet.x + Bullet.imageSize[0] / 2, 
            self.bullet.y + Bullet.imageSize[1] / 2, self.bullet.state) or 
            (self.bullet.x < 0 or self.bullet.x > self.width or 
            self.bullet.y < 0 or self.bullet.y > self.height)):            
            self.bullet.state = 0
            self.bullet.flying = False
            self.menu.life -= 1
            self.bullet.vx = Bullet.velocity * math.sin(-self.bullet.angle)
            self.bullet.vy = -Bullet.velocity * math.cos(-self.bullet.angle)
        if (self.menu.life <= 0):
            self.mode = "levelOneLose"
        elif killAll(self.target.state):
            self.mode = "levelOneWin"
        if (self.obstacle.bounceTest(self.bullet.x, self.bullet.y,
            Bullet.imageSize[0] / 2, self.bullet.state) == 1 and 
            self.bullet.bounce == False):
            self.bullet.vx = - self.bullet.vx * 0.8
            self.bullet.bounce = True
        if (self.obstacle.bounceTest(self.bullet.x, self.bullet.y,
            Bullet.imageSize[1] / 2, self.bullet.state) == 2 and
            self.bullet.bounce == False):
            self.bullet.vy = - self.bullet.vy * 0.8
            self.bullet.bounce = True
        self.target.update()

def killAll(L):
    for i in L:
        if (i > 0):
            return False
    return True    

def levelTwoPlayTimerFired(self, keysDown):
    if (not self.pause):
        self.gunner.update()
        self.obstacle2.updateNut(50)
        self.target2.updateZombie(50)
        self.bullet2.update(self.isKeyPressed, self.width, self.height)
        self.bullet2.updateSecond(100, self.isKeyPressed, self.width, self.height)
        if (self.target2.collisionTest(self.bullet2.x + Bullet.imageSize[0] / 2, 
            self.bullet2.y + Bullet.imageSize[1] / 2, self.bullet2.state)):
            self.totalScore += 30
            self.bullet2.state = 0
        if (self.target2.collisionTest(self.bullet2.secondx + Bullet.imageSize[0] / 2, 
            self.bullet2.secondy + Bullet.imageSize[1] / 2, self.bullet2.secondState)):
            self.totalScore += 30
            self.bullet2.secendState = 0
        if (self.target2.collisionTest(self.bullet2.secondx + Bullet.imageSize[0] / 2, 
            self.bullet2.secondy + Bullet.imageSize[1] / 2, self.bullet2.secondState) 
            or (self.bullet2.secondx < 0 or self.bullet2.secondx > self.width or 
            self.bullet2.secondy < 0 or self.bullet2.secondy > self.height)):
            self.bullet2.secondState = 0
            self.bullet2.secondFlying = False
        if (self.menu2.life <= 0):
            self.mode = "levelTwoLose"
        elif killAll(self.target2.state):
            self.mode = "levelTwoWin"
        if (self.target2.collisionTest(self.bullet2.x + Bullet.imageSize[0] / 2, 
            self.bullet2.y + Bullet.imageSize[1] / 2, self.bullet2.state) or 
            (self.bullet2.x < 0 or self.bullet2.x > self.width or 
             self.bullet2.y < 0 or self.bullet2.y > self.height)):
            self.bullet2.state = 0
            self.bullet2.flying = False
            self.menu2.life -= 1
        if (self.obstacle2.bounceTest(self.bullet2.secondx - 20, self.bullet2.secondy,
            Bullet.imageSize[0] / 2, self.bullet2.secondState) == 1 and 
            self.bullet2.secondBounce == False):
            self.bullet2.secondvx = - self.bullet2.secondvx * 0.8
            self.bullet2.secondBounce = True
        if (self.obstacle2.bounceTest(self.bullet2.secondx- 20, self.bullet2.secondy,
            Bullet.imageSize[0] / 2, self.bullet2.secondState) == 2 and
            self.bullet2.secondBounce == False):
            self.bullet2.secondvy = - self.bullet2.secondvy * 0.8
            self.bullet2.secondBounce = True
        if (self.obstacle2.bounceTest(self.bullet2.x- 20, self.bullet2.y,
            Bullet.imageSize[0] / 2, self.bullet2.state) == 1 and 
            self.bullet2.bounce == False):
            self.bullet2.vx = - self.bullet2.vx * 0.8
            self.bullet2.bounce = True
        if (self.obstacle2.bounceTest(self.bullet2.x- 20, self.bullet2.y,
            Bullet.imageSize[0] / 2, self.bullet2.state) == 2 and
            self.bullet2.bounce == False):
            self.bullet2.vy = - self.bullet2.vy * 0.8
            self.bullet2.bounce = True        
        self.target2.update()

def levelThreePlayTimerFired(self, keysDown):
    if (not self.pause):
        self.obstacle3.updateNut(50)
        self.target3.updateZombie(50)
        self.obstacle3.updateBlower(50)
        self.bullet3.launch(self.keyDown)    
        self.gunner.update()
        self.bullet3.bullet3Update(self.keyDown, self.width, self.height)
        if (self.target3.collisionTest(self.bullet3.x + Bullet.imageSize[0] / 2, 
            self.bullet3.y + Bullet.imageSize[1] / 2, self.bullet3.state)):
            self.totalScore += 30
            self.bullet3.state = 0
        if (self.target3.collisionTest(self.bullet3.x + Bullet.imageSize[0] / 2, 
            self.bullet3.y + Bullet.imageSize[1] / 2, self.bullet3.state) or 
            (self.bullet3.x < 0 or self.bullet3.x > self.width or 
             self.bullet3.y < 0 or self.bullet3.y > self.height)):
            self.bullet3.state = 0
            self.bullet3.flying = False
            self.menu3.life -= 1
        if (self.menu3.life <= 0):
            self.mode = "levelThreeLose"
        elif killAll(self.target3.state):
            self.mode = "levelThreeWin"
        if (self.obstacle3.bounceTest(self.bullet3.x, self.bullet3.y,
            Bullet.imageSize[0] / 2, self.bullet3.state) == 1 and 
            self.bullet3.bounce == False):
            self.bullet3.vx = - self.bullet3.vx * 0.8
            self.bullet3.bounce = True
        if (self.obstacle3.bounceTest(self.bullet3.x, self.bullet3.y,
            Bullet.imageSize[0] / 2, self.bullet3.state) == 2 and
            self.bullet3.bounce == False):
            self.bullet3.vy = - self.bullet3.vy * 0.8
            self.bullet3.bounce = True
        self.target3.update()

################################################################################ 
def homeRedrawAll(self, screen):
    self.home.drawButton(screen, self.bestScore)
    if (self.backToHome == True):
        self.home.drawBackToGame(screen)

def helpRedrawAll(self, screen):
    self.help.draw(screen)
    self.help.drawBack(screen)

def levelOnePlayRedrawAll(self, screen): 
    self.menu.draw(screen)
    self.menu.drawLongLawn(screen)   
    self.gunner.draw(screen)  
    self.obstacle.draw(screen)
    self.menu.drawScore(screen, self.totalScore)
    self.menu.drawLevel(screen, 1)
    self.menu.drawButtonHelp(screen)            
    self.target.draw(screen)
    self.bullet.draw(screen)
    self.menu.drawPause(screen, self.pause, self.put)
    self.menu.drawPut(screen, self.put)  
    self.obstacle.drawPut(screen, self.put, self.drag)
    self.menu.drawReminder(screen, self.start)

def loseRedrawAll(self, screen):
    self.lose.draw(screen)
    self.lose.drawLose(screen)

def levelOneWinRedrawAll(self, screen):
    self.win.draw(screen)
    self.win.drawWin(screen)

def levelThreeWinRedrawAll(self, screen): 
    self.win.draw(screen)
    self.win.drawEnd(screen)

def levelTwoPlayRedrawAll(self, screen):   
    self.menu2.draw(screen)
    self.menu2.drawLongLawn(screen)  
    self.gunner.draw(screen)
    self.obstacle2.draw(screen)
    self.menu2.drawScore(screen, self.totalScore)
    self.menu2.drawLevel(screen, 2)
    self.menu2.drawButtonHelp(screen) 
    self.target2.draw(screen)  
    self.bullet2.draw(screen)
    self.bullet2.drawSecondBullet(screen)
    self.menu2.drawPause(screen, self.pause, self.put)
    self.menu.drawPut(screen, self.put)
    self.obstacle2.drawPut(screen, self.put, self.drag)
    self.menu2.drawReminder(screen, self.start)

def levelThreePlayRedrawAll(self, screen): 
    self.menu3.draw(screen)
    self.menu3.drawLongLawn(screen) 
    self.gunner.draw(screen)
    self.obstacle3.draw(screen)
    self.obstacle3.drawBlower(screen)
    self.menu3.drawScore(screen, self.totalScore)
    self.menu3.drawLevel(screen, 3) 
    self.menu3.drawButtonHelp(screen)
    self.target3.draw(screen)  
    self.bullet3.draw(screen)
    self.bullet3.drawEngyBar(screen)
    self.menu.drawPause(screen, self.pause, self.put)
    self.menu.drawPut(screen, self.put)
    self.obstacle3.drawPut(screen, self.put, self.drag)
    self.menu3.drawReminder(screen, self.start)

################################################################################ 
## main function
################################################################################
class Game(PygameGame):
    def init(self):
        self.bestScore = getBestScore()      
        self.mode = "home"
        self.lastMode = None
        self.pause = False
        self.keyDown = None
        self.put = False
        self.drag = False
        self.alreadyPut = False
        self.start = False
        self.backToHome = False
        
        Menu.scoreInit()  
        Menu.PicInit() 
        self.home = Menu(0, 0, 'home.jpg')
        self.help = Menu(0, 0, 'help.jpg')
        self.menu = Menu(0, 0, 'background1 copy.jpg')
        self.menu2 = Menu(0, 0, 'background22 copy.jpg')
        self.menu3 = Menu(0, 0, 'background3.jpg')

        self.lose = Menu(0, 0, 'lose1.png')   
        self.win = Menu(0, 0, 'win.png')    
        self.gunner = Gunner(10, 450)

        Bullet.animation()
        self.bullet = Bullet(100, 500)
        self.bullet2 = Bullet(100, 500)
        self.bullet3 = Bullet(100, 500)

        Obstacle.init()
        self.obstacle = Obstacle('nut.png')
        self.obstacle2 = Obstacle('nut.png')
        self.obstacle3 = Obstacle('nut.png')

        Target.init()
        self.target = Target()
        self.target2 = Target()
        self.target3 = Target()

        self.totalScore = 0

        pygame.mixer.music.load("1.wav")
        pygame.mixer.music.play(-1)
        
    def mousePressed(self, x, y):
        if (self.mode == "home"): homeMousePressed(self, x, y)
        elif (self.mode == "help"): helpMousePressed(self, x, y)
        elif (self.mode == "levelOnePlay"): levelOnePlayMousePressed(self, x, y)
        elif (self.mode == "levelOneLose"): levelOneLoseMousePressed(self, x, y)
        elif (self.mode == "levelOneWin"): levelOneWinMousePressed(self, x, y)
        elif (self.mode == "levelTwoPlay"): levelTwoPlayMousePressed(self, x, y)
        elif (self.mode == "levelTwoLose"): levelTwoLoseMousePressed(self, x, y)
        elif (self.mode == "levelTwoWin"): levelTwoWinMousePressed(self, x, y)
        elif (self.mode == "levelThreePlay"): levelThreePlayMousePressed(self, x, y)
        elif (self.mode == "levelThreeLose"): levelThreeLoseMousePressed(self, x, y)
        elif (self.mode == "levelThreeWin"): levelThreeWinMousePressed(self, x, y)

    def mouseReleased(self, x, y):
        if (not self.pause):
            pygame.mixer.music.unpause() 
        if (self.mode == "levelOnePlay"): levelOnePlaymouseReleased(self, x, y)
        elif (self.mode == "levelTwoPlay"): levelTwoPlaymouseReleased(self, x, y)
        elif (self.mode == "levelThreePlay"): levelThreePlaymouseReleased(self, x, y)
        
    def mouseDrag(self, x, y):
        if (self.mode == "levelOnePlay"): levelOnePlayMouseDrag(self, x, y)
        elif (self.mode == "levelTwoPlay"): levelTwoPlayMouseDrag(self, x, y)
        elif (self.mode == "levelThreePlay"): levelThreePlayMouseDrag(self, x, y)

    def keyPressed(self, code, mod):
        self.keyDown = self._keys[32]

    def keyReleased(self, code, mod):
        self.keyDown = self._keys[32]

    def timerFired(self, keysDown):
        if (self.mode == "home"): homeTimerFired(self, keysDown)
        elif (self.mode == "levelOnePlay"): levelOnePlayTimerFired(self, keysDown)
        elif (self.mode == "levelTwoPlay"): levelTwoPlayTimerFired(self, keysDown)
        elif (self.mode == "levelThreePlay"): 
            levelThreePlayTimerFired(self, keysDown)

    def redrawAll(self, screen):
        self.screen = screen
        if (self.mode == "home"): homeRedrawAll(self, screen)
        elif (self.mode == "help"): helpRedrawAll(self, screen)
        elif (self.mode == "levelOnePlay"): levelOnePlayRedrawAll(self, screen)
        elif (self.mode == "levelOneLose"): loseRedrawAll(self, screen)
        elif (self.mode == "levelOneWin"): levelOneWinRedrawAll(self, screen)
        elif (self.mode == "levelTwoPlay"): levelTwoPlayRedrawAll(self, screen)
        elif (self.mode == "levelTwoLose"): loseRedrawAll(self, screen)
        elif (self.mode == "levelTwoWin"): levelOneWinRedrawAll(self, screen)
        elif (self.mode == "levelThreePlay"): 
            levelThreePlayRedrawAll(self, screen)
        elif (self.mode == "levelThreeLose"): loseRedrawAll(self, screen)
        elif (self.mode == "levelThreeWin"): levelThreeWinRedrawAll(self, screen)

Game(800, 600).run()