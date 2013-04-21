import pygame
from pygame.locals import*
from Accessories import*

#need the key repeat enable thing (might need more constants for that)


WWD=400
WHT=800
WHITE=(255,255,255)
BLACK=(0,0,0)
FPS=40
UPC=1   #updates per cycle



class Phynball:
    def __init__(self,size=(WWD,WHT)):
        pygame.init()
        self.screen=pygame.display.set_mode(size)
        self.state=0    # state as in opening, main, ending screens
        self.clock=pygame.time.Clock()
        self.fps=FPS
        self.refr=True      #tells to refresh screen or not
        self.fill=WHITE
        self.dt=1.0/(FPS*UPC)

        self.balls=[]
        self.flippers=[]
        self.walls=[]
        self.fields=[]
        self.cam=None
        initialize(self)       #found in accessories file

                

    def handle(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                self.state=-1
            elif event.type==KEYDOWN:
                self.keyDown(event.key)
            elif event.type==KEYUP:
                self.keyUp(event.key)
            elif event.type==MOUSEBUTTONUP:
                self.mouseUp(event.button,event.pos)

    def run(self):
        while self.state!=-1:
            if self.state==0:
                self.openingScreen()
            elif self.state==1:
                self.mainloop()
            elif self.state==2:
                self.mainloop()
                
    def openingScreen(self):
        while self.state==0:
            self.openhandle()
            self.opendraw()
            self.openupdate()
            pygame.display.flip()
            self.clock.tick(FPS)



    def openhandle(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                self.state=-1 #immediately forgo other loops
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE: #go to mainloop
                    self.state=1
                else:
                    self.openkeydown(event.key)
            if event.type==KEYUP:
                self.openkeyup(event.key)
            if event.type==MOUSEBUTTONUP:
                self.openmouseup(event.button,event.pos)


    def opendraw(self):
        pass



    

    def openupdate(self):
        pass





    def openkeydown(self,key):
        pass





    def openkeyup(self,key):
        pass




    
    def openmouseup(self,button,pos):
        pass


















        
    def mainloop(self):
        #add pause function
        while self.state==1:
            pygame.display.set_caption('FPS: %i'%self.clock.get_fps())
            self.handle()
            self.draw()
            for i in range(UPC):
                self.update()
            pygame.display.flip()
            self.clock.tick(self.fps)

        #eventually add stuff to enable going back to opening screen

    def closingScreen(self):
        self.state=-1 #nothing goes on here yet
        while self.state==2:
            pass
        


    def update(self):
        for f in self.fields:
            f.func(self.balls)

        for b in self.balls:
            b.update(self.dt)

        darc(self)  #detect and resolve collisions (found in accessories)

        self.cam.update(self.balls)
        pass
                 
    def draw(self):
        if self.refr:
            self.screen.fill(self.fill) #later to be replaced with background

        for w in self.walls:
            w.draw(self.screen,self.cam)
        for f in self.flippers:
            f.draw(self.screen,self.cam)
        for b in self.balls:
            b.draw(self.screen,self.cam)
        
                     
    def keyDown(self, key):
        pass
        
    def keyUp(self, key):
        pass
        
    def mouseUp(self, button, pos):
        pass
        
    def mouseMotion(self, buttons, pos, rel):          
        pass


    


Phy=Phynball()
Phy.run()
pygame.quit()
