# script that runs the game

from pygamehelper import *
import pygame
from pygame.locals import *
from math import pi, cos, sin, sqrt, atan
from random import uniform, choice
from accessories_final import *
from powerups_final import*



class Game(PygameHelper):       # see PygameHelper script
    def __init__(self):
        self.w, self.h = screenwidth, screenheight
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

        # initialize various constants that will come into play throughout the game
        self.dt=dt_strd                 # time increment
        self.time=0                     # game clock
        self.bord_color_override=()     # (see draw)
        self.refresh=True               # (see draw)

        self.balls=[]
        self.borders=[]
        self.forcefields=[]
        self.flippers=[]
        self.sinks=[]
        self.powerups=[]
        self.icons=[]

        
        self.balls.append(ball_obj((screenwidth-86,400),(0,0),radius=30))       # initialize ball
        self.borders=initializeBorder()                                     # initialize borders
        self.forcefields.append(force_field(grav))                          # initialize gravity
        #self.flippers=initializeFlippers()                                  # initialize flippers
        #self.sinks=initializeSinks()                                        # initialize sinks

        
    def update(self):
        if len(self.balls)==0:
            print 'Game Over! Press y for new ball'              # game ends when there are no balls left onscreen
            if pygame.key.get_pressed()[K_y]:
                print 'y'
                new_ball=ball_obj((uniform(randompos,screenwidth-randompos),uniform(randompos,screenheight-3*randompos)),(uniform(-randomvel,randomvel),uniform(-randomvel,randomvel)))
                self.balls.append(new_ball)
        # loop over all balls
        for ball in self.balls:
            netacc=vec((0,0))               # net acceleration starts out as 0
            for field in self.forcefields:  # loop over all forcefields
                acc=field.force(ball)
                netacc +=acc                 # sum contributions of each forcefield to net acceleration
                
            ball.vel+=netacc*self.dt        # increments the velocity based on net acceleration
            ball.pos+=ball.vel*self.dt      # increments position based on velocity
            
            if ball.pos[0]<0 or ball.pos[0]>screenwidth or ball.pos[1]<0 or ball.pos[1]>screenheight:
                # resolution of ball leaving game zone by clipping through the walls:
                # ball is teleported back into play at a random position and with a random speed
                ball.pos=vec((uniform(randompos,screenwidth-randompos),uniform(randompos,screenheight-randompos*3)))
                ball.vel=vec((uniform(-randomvel,randomvel),uniform(-randomvel,randomvel)))
                print 'Warp Factor!'
            

            for bord in self.borders:       # loop over all borders for collision detection
                collision_detect_resolve(bord,ball)  
            for flipper in self.flippers:   # loop over all flippers for collision detection
                collision_flipper(flipper,ball)

                
        
        # updates the list of balls to include only those that have not fallen into a sink
        self.balls[:]=[ball for ball in self.balls if not remove_ball(ball,self.sinks)]
        
        for flipper in self.flippers:       # loop over flippers to handle their motion
            update_flipper(flipper,pygame.key.get_pressed())


        new_icon(self)                      # creates a new icon if conditions are fulfilled
        
        for icon in self.icons:             # loop over icons to reduce their life
            icon.life-=1

        # updates the list of icons to include only those that have not been obtained or expired
        self.icons[:]=[icon for icon in self.icons if icon_ball(icon,self)]
            
        for powerup in self.powerups:       # loop over powerups
            if powerup.time_left==1:
                powerup.reset(self)         # if a powerup is about to end, it executes its reset commands
            else:
                if (powerup.time_left%powerup.do_every==0):
                    powerup.commands(self)  # otherwise it will execute its commands every do_every updates
                    print powerup.name      # tells the player which powerup is active
                    
            powerup.time_left-=1            # reduce the life of the powerup

        # updates the list of powerups to include only those that have not ended
        self.powerups[:]=[powerup for powerup in self.powerups if powerup.time_left>0]

        self.time+=1                        # update game clock
        
    def keyDown(self, key):
        if key==27:                         # ends the game if escape key has been pressed (safe way to end game)
            quit()

    def draw(self):
        if self.refresh:                    # refreshes the screen if refresh property is true
            self.screen.fill((255,255,255))
            
        
        for ball in self.balls:             # loop over balls,
            
            pygame.draw.circle(self.screen,(0,0,0),ball.pos.rtup(),ball.rad+1)  # to draw outline,
            pygame.draw.circle(self.screen,ball.col,ball.pos.rtup(),ball.rad)   # and then middle part of ball


        for sink in self.sinks:             # loop over sinks to draw rectangular and circular sinks
            if sink.shape=='rect':
                pygame.draw.rect(self.screen,sink.color,sink.dimensions)
            if sink.shape=='circ':
                pygame.draw.circle(self.screen,sink.color,sink.dimensions[0],sink.dimensions[1])

        for bord in self.borders:           # loop to draw borders
            b_color=self.bord_color_override or bord.col    # if bord_color_override is empty, color will be bord.col
            
            if bord.shape=='rect':
                pygame.draw.rect(self.screen,b_color,bord.vertices)     
            else:
                pygame.draw.polygon(self.screen,b_color,bord.vertices)

        for flip in self.flippers:          # loop to draw flippers
            draw_flipper(flip,self.screen)

        for icon in self.icons:             # loop to draw icons
            pygame.draw.circle(self.screen,icon.col,icon.pos.rtup(),icon.rad)
        

# creates the Game object and starts game
Phynball = Game()
Phynball.mainLoop(FPS)
