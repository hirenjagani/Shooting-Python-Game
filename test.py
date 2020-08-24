import pygame
import random
from pygame.locals import*
global screen
import os,sys
import splashscreen

pygame.init()

#Display the Window on Screen

screen=pygame.display.set_mode((400,400))
WINDOWWIDTH=400
window=screen
WINDOWHEIGHT=400
SCORE=0
#Color Used for GAME START and GAME END

skyblue=(1,74,112)
black=BLACK=(0,0,0)
WHITE=white=(255,255,255)
red=RED=(255,0,0)
blue=(0,0,255)

#To Quit

def terminate():
    pygame.quit()
    sys.exit()
    
def message_to_screen(msg,color):
      font=pygame.font.SysFont(None, 60)
      screen_text=font.render(msg,True,skyblue)
      window.blit(screen_text,[70,300])
      
#GAME OVER FUNCTION

def showGameOverScreen(SCORE):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game', True, red)
    overSurf = gameOverFont.render('Over', True, red)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            runGame() # clear event queue
            return

#Checks For Any Key Press 

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


    
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, blue)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (100, 350)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


#Shows Start Screen 

def showStartScreen():
    titleFont = pygame.font.Font(None, 72)
    titleSurf1 = titleFont.render('COMMANDO', True, WHITE, skyblue)
    titleSurf2 = titleFont.render('SHOOTING', True, blue)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(white)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() 
            return
        pygame.display.update()
        FPSCLOCK.tick(10)
        degrees1 += 3 
        degrees2 += 7
def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False

#Loads the Image From the Path

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image,image.get_rect()
global limg,rimg,climg,crimg,rrimg,rlimg
#Left Image
limg=[load_image("STL1.bmp",-1),load_image("STL2.bmp",-1),load_image("STL3.bmp",-1)]
#Right Image
rimg=[load_image("STR1.bmp",-1),load_image("STR2.bmp",-1),load_image("STR3.bmp",-1)]
#Counter Left
climg=[load_image("CTL1.bmp",-1),load_image("CTL2.bmp",-1),load_image("CTL3.bmp",-1)]
#Counter Right
crimg=[load_image("CTR1.bmp",-1),load_image("CTR2.bmp",-1),load_image("CTR3.bmp",-1)]
#Rotate Right 
rrimg=[load_image("RR1.bmp",-1),load_image("RR2.bmp",-1),load_image("RR3.bmp",-1)]
#Rotate Left
rlimg=[load_image("RL1.bmp",-1),load_image("RL2.bmp",-1),load_image("RL3.bmp",-1)]

#OPPONENT PLAYER  FUNCTION

class rebel(pygame.sprite.Sprite):


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        c,self.rect=rrimg[1]
        self.x=random.randint(150,250)
        self.y=random.randint(-200,0)

        self.y=self.y*3  #Timer
        self.facing=random.randint(0,1)
        if self.facing==1:
            self.facing="r"  #Face Left 
        else:
            self.facing="l"  #Face Right
        self.moving=False
        self.inum=2
        self.jumping=True
        self.shooting=False
        self.jmomentum=9
        self.imgmod=.5
        self.rect.topleft=(self.x,self.y)
        self.timer=0
        self.saw=False
        self.moveturn=0
        self.moveturnl=random.randint(60,60)
        if self.facing=="r":
            self.image,c=rrimg[1]
        else:
            self.image,c=rlimg[1]
        self.platform=True


    def update(self):
        if self.x>395:
            self.x=0
        elif self.x<0:
            self.x=395
        if self.y+11<=Player.y+22 and self.y+11>=Player.y:
            if self.saw:
                self.shooting=True
            elif self.facing=="r" and Player.x>self.x:
                self.shooting=True
                self.saw=1
            elif self.facing<>"r" and Player.x<self.x:
                self.shooting=True
                self.saw=1
        else:
            self.shooting=False
        if self.timer<10:
            self.timer+=1
        if self.saw:
            if self.y<Player.y:
                self.moving=True
            elif self.y>Player.y:
                self.moving=True
                if self.x<110 and self.x>90:
                    if not self.jumping:
                        self.jmomentum=10
                        self.jumping=True

                elif self.x>290 and self.x<310:
                    if not self.jumping:
                        self.jmomentum=10
                        self.jumping=True
            if self.shooting:
                if self.x<Player.x:
                    self.facing="r"
                elif self.x>Player.x:
                    self.facing="l"
                
        else:
            if pygame.sprite.spritecollide(self,floors,0):
                self.moving=True
                self.moveturn+=1
                if self.moveturn==self.moveturnl:
                    if self.facing=="r":
                        self.facing="l"
                    else:
                        self.facing="r"
                    self.moveturn=0
            else:
                self.moving=False
                if self.platform:
                    self.platform=False
                else:
                    self.platform=True
                
        if self.moving:
            if self.facing=="r":
                self.x+=3
            else:
                self.x-=3
            self.inum+=self.imgmod
            if self.inum>3:
                self.imgmod=-.5
                self.inum=2.5
            elif self.inum<1:
                self.imgmod=.5
                self.inum=1
        else:
            self.inum=2
        if self.jumping==True:
            self.jump()
        if self.facing=="r":
            self.image,c=rrimg[int(round(self.inum-1))]
        else:
            self.image,c=rlimg[int(round(self.inum-1))]
        self.rect.topleft=(self.x,self.y)
        if not pygame.sprite.spritecollide(self,floors,0):
            self.jumping=True
        if self.shooting:
            if self.timer==10:
                if self.facing=="r":
                    speed=10
                    facecompromise=10
                else:
                    speed=-10   
                    facecompromise=0
                self.timer=0
                enemybullets.add(playerbullet(self.x+facecompromise,self.y+11,speed))
                    
        if pygame.sprite.spritecollide(self,playerbullets,1):
            
            enemygroup.add(rebel())
            pygame.sprite.Sprite.kill(self)
        
    def jump(self):
        self.y-=self.jmomentum
        if pygame.sprite.spritecollide(self,floors,0):
            for x in floors:
                if self.jmomentum<0 and self.y<x.rect.topleft[1] and self.y-self.jmomentum>x.rect.topleft[1]-21 and self.x<x.rect.topright[0] and self.x>x.rect.topleft[0]-11:
                    self.y=x.rect.topleft[1]-21
                    self.jumping=False
        self.jmomentum-=1
        if self.jmomentum<-10:
            self.jmomentum=-10
        

#PLAYER FUNCTION

class stormtrooper(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x=0
        self.y=378
        self.facing="r"
        self.moving=False
        self.rect=pygame.rect.Rect(self.x,self.y,19,23)
        self.inum=2
        self.jumping=False
        self.jumplimit=self.rect.topleft[1]-14
        self.jmaxed=0
        self.jmomentum=9
        self.imgmod=.5
        self.life=3

    def update(self):
        if self.x>395:
            self.x=0
        elif self.x<0:
            self.x=395
        if self.moving:
            if self.facing=="r":
                self.x+=3
            else:
                self.x-=3
            self.inum+=self.imgmod
            if self.inum>3:
                self.imgmod=-.5
                self.inum=2.5
            elif self.inum<1:
                self.imgmod=.5
                self.inum=1
        else:
            self.inum=2
        if self.jumping==True:
            self.jump()
        if self.facing=="r":
            self.image,c=rimg[int(round(self.inum-1))]
        else:
            self.image,c=limg[int(round(self.inum-1))]
        self.rect.topleft=(self.x,self.y)
        if not pygame.sprite.spritecollide(self,floors,0):
            self.jumping=True
        if pygame.sprite.spritecollide(self,enemybullets,1):
            self.x=0
            self.y=378
            showGameOverScreen(SCORE)
            
    def jump(self):
        self.y-=self.jmomentum
        if pygame.sprite.spritecollide(self,floors,0):
            for x in floors:
                if self.jmomentum<0 and self.y<x.rect.topleft[1] and self.y-self.jmomentum>x.rect.topleft[1]-21 and self.x<x.rect.topright[0] and self.x>x.rect.topleft[0]-11:
                    self.y=x.rect.topleft[1]-21
                    self.jumping=False
                    
        self.jmomentum-=1
        if self.jmomentum<-10:
            self.jmomentum=-10

#Floor            
            
class floor(pygame.sprite.Sprite):
    def __init__(self,startpos,endpos,thickness=5):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((endpos[0]-startpos[0],thickness))
        self.rect=self.image.get_rect(topleft=startpos)
        self.image.fill((255,255,255))

#Player Bullet Function

class playerbullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.y=y
        self.x=x
        self.speed=speed
        self.image,self.rect = load_image("laser.bmp",-1)
        self.rect.topleft=(self.x,self.y)
        self.life=3
    def update(self):
        self.x+=self.speed
        self.rect.topleft=(self.x,self.y)
        if self.x<-10 or self.x>410:
            pygame.sprite.Sprite.kill(self)
            
Player=stormtrooper()

clock=pygame.time.Clock()
pgroup=pygame.sprite.RenderPlain(Player)

enemygroup=pygame.sprite.RenderPlain(rebel())
playerbullets=pygame.sprite.RenderPlain()

enemybullets=pygame.sprite.RenderPlain()
j=1

#Set Caption on the Top

pygame.display.set_caption("SHOOTING")

#Floors Co-ordinates

floors=pygame.sprite.RenderPlain(floor((0,395),(400,395)),
                                 floor((300,350),(400,350)),
                                 floor((0,350),(100,350)),
                                 floor((110,300),(290,300)),
                                 floor((0,250),(100,250)),
                                 floor((300,250),(400,250)),
                                 floor((110,200),(290,200)),
                                 floor((0,150),(100,150)),
                                 floor((300,150),(400,150)),
                                 floor((110,100),(290,100)))

#Game Run 

def runGame ():
    '''
    Player=stormtrooper()

    clock=pygame.time.Clock()
    pgroup=pygame.sprite.RenderPlain(Player)

    enemygroup=pygame.sprite.RenderPlain(rebel())
    playerbullets=pygame.sprite.RenderPlain()

    enemybullets=pygame.sprite.RenderPlain()
    j=1
    pygame.display.set_caption("SHOOTING")
    
    floors=pygame.sprite.RenderPlain(floor((0,395),(400,395)),
                                     floor((300,350),(400,350)),
                                     floor((0,350),(100,350)),
                                     floor((110,300),(290,300)),
                                     floor((0,250),(100,250)),
                                     floor((300,250),(400,250)),
                                     floor((110,200),(290,200)),
                                     floor((0,150),(100,150)),
                                     floor((300,150),(400,150)),
                                     floor((110,100),(290,100)))
    '''                                
    clock.tick(30)
    for event in pygame.event.get():

        if event.type==KEYDOWN:

            if event.key==K_LEFT:   #Left 

                Player.facing="l"
                Player.moving=True

            if event.key==K_RIGHT:  #Right

                Player.facing="r"
                Player.moving=True

            if event.key==K_UP:     #up or jump

                if Player.jumping<>True:

                    Player.jmomentum=10

                Player.jumping=True

            if event.key==K_ESCAPE: #Quit

                showGameOverScreen(0)

            if event.key==K_SPACE:  #Shoot Bullets

                if Player.facing=="r":

                    speed=10
                    facecompromise=10

                else:
                    speed=-10
                    facecompromise=0

                playerbullets.add(playerbullet(Player.x+facecompromise,Player.y+11,speed))

        if event.type==KEYUP:

            if event.key==K_LEFT and Player.facing=='l':

                Player.moving=False

            elif event.key==K_RIGHT and Player.facing=='r':

                Player.moving=False

        if event.type==QUIT:

            j=0

        else:

            break

    screen.fill((skyblue))
    pgroup.update()
    enemygroup.update()
    
    
    playerbullets.update()
    enemybullets.update()
    playerbullets.draw(screen)
    
    enemybullets.draw(screen)
    floors.draw(screen)
    pgroup.draw(screen)
    
    enemygroup.draw(screen)
    pygame.display.update()
    

#MAIN FUNCTION OF GAME>


def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT,y,life
        
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF =screen
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('SHOOTING')
    splashscreen.splash_screen() 
    showStartScreen()

    while True:
        runGame()
    enemygroup.add(rebel())
    pygame.sprite.Sprite.kill(rebel())
    showGameOverScreen(0)
        
if __name__ == '__main__':
    main()
