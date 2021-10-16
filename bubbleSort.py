import sys, pygame
from pygame.draw import circle
from pygame.locals import *
import time
import math

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

size = width, height = 500, 500
radius = 25
speed = 0.01
BLACK = 0, 0, 0
RED = (159, 0, 15)
numbers = ['','','','','']
screen = pygame.display.set_mode(size)

angle = 0
i = 0
j = 1

index = 0
rotate = False
circleCount = 5
text = '1'
font = pygame.font.SysFont(None, 48)
img = font.render(text, True, RED)

rect = img.get_rect()
rect.topleft = (20, 20)
cursor = Rect(rect.topright, (3, rect.height))


screen.fill((236,229,182))


class Circle():
    def __init__(self, width , height , radius):
        self.x = width
        self.y = height
        self.px = width
        self.py = height
        self.radius = radius

    def new(self , screen):
        pygame.draw.circle(screen , RED , (self.x , self.y) , self.radius)


    def move(self , right):

        if right : direct = -1
        else: direct = 1
        global angle
        self.x = direct * int(width/12 * math.cos(angle)) + (self.px - (direct)*width/12)
        self.y = direct * int(-width/12 * math.sin(angle)) + self.py
    
class Number():
    def __init__(self , number ,x , y):
        self.x = x
        self.y = y
        self.px = x
        self.py = y
        self.num = number

    def new(self):
        num1 = myfont.render(self.num , False , pygame.Color('black'))
        screen.blit(num1, (self.x , self.y))

    def move(self , right):
        if right: direct = -1
        else: direct = 1
        global angle
        if angle <= math.pi:
            self.x = direct * int(width/12 * math.cos(angle)) + (self.px - (direct)*width/12)
            self.y = direct * int(-width/12 * math.sin(angle)) + self.py


circles = [Circle(i*width/(circleCount+1), height/2 , radius) for i in range(1 , circleCount+1)]
texts = [Number(numbers[i] , (i+1) * width/6 - radius/3 , height/2- radius) for i in range(circleCount)]



def drawCircles():
    for circle in circles:
        circle.new(screen)
def drawNumbers():
    for text in texts:
        text.new()

def drawObj():
    drawCircles()
    drawNumbers()
def moveObj(i):
    global angle
    global rotate
    if angle <= math.pi:
        texts[i].move(True)
        circles[i].move(True)
        texts[i-1].move(False)
        circles[i-1].move(False)
        angle += math.pi/15
    else:
        angle = 0
        circles[i].px = circles[i].x
        texts[i].px = texts[i].x
        circles[i-1].px = circles[i-1].x
        texts[i-1].px = texts[i-1].x
        rotate = False

def textBox():
    screen.blit(img,rect)
    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, RED, cursor)

def swap(i):
    numbers[i] , numbers[i+1] = numbers[i+1] , numbers[i]
    circles[i] , circles[i+1] = circles[i+1] , circles[i]
    texts[i] , texts[i+1] = texts[i+1] , texts[i]
    


while 1:
    msElapsed = clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
        if event.type == KEYDOWN and index < 5:
            if event.key == K_BACKSPACE:
                if len(text)>0:
                    text = text[:-1]
            elif event.key == K_RETURN:
                numbers[index] = text
                texts[index].num = text
                text = ''
                index += 1
            else:
                text += event.unicode
            img = font.render(text, True, RED)
            rect.size=img.get_size()
            cursor.topleft = rect.topright
    screen.fill((236,229,182))
    if index < 5:
        textBox()
    else:
        end = circleCount - j
        if not rotate:
            if i < end:  
                if int(numbers[i]) > int(numbers[i+1]):
                    swap(i)
                    rotate = True
                i+=1
            elif i == end:
                i = 0
                j+=1

        else:
            moveObj(i)

    drawObj()
    if j==circleCount-1:
        numx = myfont.render('game over' , False , pygame.Color('black'))
        screen.blit(numx, (150 , 30))
    pygame.display.update()