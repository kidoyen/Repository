# this file documents "Powerups" which influence the behavior of the game (they can help the player or impede them).
# they will first appear as circles on the screen and the player will have
# to "get" them by hitting them with the ball to make them activate

from accessories_final import*
from random import uniform,choice
import pygame


one_time=2                  # powerup has a one-time effect and then disappears
short_life=5*FPS            # 5 second lifespan
med_life=15*FPS             # 15 second lifespan
long_life=60*FPS            # 60 second lifespan
each_update=1               # indicates the powerup will have a continuous effect every update
time_bet_powerups=3*FPS     # max time to wait between sending out another powerup

icon_rad=30                 # poweups will appear as circles with this radius


# used as default for powerup commands
def empty(anything=0):
    pass

# creates a color that smoothly changes over time
def rainbow(t):
    freq=1/50.0
    R=127*sin(freq*t+0)+128
    G=127*sin(freq*t+2)+128
    B=127*sin(freq*t+4)+128
    return int(R),int(G),int(B)

# random color used when an icon is initialized
def rand_color():
    return uniform(0,255),uniform(0,255),uniform(0,255)

# class used to describe how the powerup will appear onscreen
class power_up_icon():
    def __init__(self,position=vec((screenwidth/2,screenheight/2)),radius=icon_rad,life=med_life,color=rand_color(),powerup_ind=-1):
        self.pos=position           # currently the icon will only appear in the middle of the screen and will be stationary
        self.rad=radius
        self.life=life              # how long the icon will wait before disappearing
        self.col=color
        self.ind=powerup_ind        # references which powerup to implement (-1 means choose a random one)

# creates a new icon under certain conditions
def new_icon(gamestate):
    if len(gamestate.powerups)==0 and len(gamestate.icons)==0 and (gamestate.time%time_bet_powerups==0):
        # currently, powerups will not be emitted if there are unobtained icons onscreen or if there is already a powerup active
        # time%time_bet ensures there will be a delay between when a powerup ends and when the next powerup is emitted
        gamestate.icons.append(power_up_icon())

# removes an icon and implements the powerup when the ball obtains the icon
# also removes icon if it has not been obtained by the end of its life
def icon_ball(icon,gamestate):
    for ball in gamestate.balls:
        if icon.life<=0:
            return False
        if modulus(icon.pos-ball.pos)>(icon.rad+ball.rad):
            return True
        if icon.ind!=-1:
            gamestate.powerups.append(power_up(all_powerups[icon.ind]))     # chooses the powerup at the specified index in the list if index is not -1
        else:
            gamestate.powerups.append(power_up(choice(all_powerups)))       # otherwise chooses a random powerup
        return False
    
# defines the actual powerup efects
class power_up():
    def __init__(self,p_info):      # info is received through a list
        self.commands=p_info[0]     # commands to execute when initialized (and whenever asked to repeat commands)
        self.reset=p_info[1]        # commands to fix what was done
        self.time_left=p_info[2]    # time left until the powerup ends
        self.do_every=p_info[3]     # how often to repeat commands (setting this equal to the lifetime will ensure it is a one time effect)
        self.name=p_info[4]         # name of powerup


def WoodStock_commands(gamestate):
    gamestate.dt=dt_strd/3                                      # slows down phsyics
    gamestate.refresh=False                                     # creates a trailing effect of the ball and flippers
    gamestate.bord_color_override=rainbow(gamestate.time)       # makes the borders change colors
    
def WoodStock_reset(gamestate):     # undoes everything above
    gamestate.dt=dt_strd
    gamestate.refresh=True
    gamestate.bord_color_override=()

# all properties are packaged in a list. This powerup will last 5 seconds and will execute every update (to continuously change the border colors)
wood_stock=[WoodStock_commands,WoodStock_reset,short_life,each_update,'WoodStock']



def zeroG_commands(gamestate):
    del gamestate.forcefields[0]    # takes gravity away
    
def zeroG_reset(gamestate):
    gamestate.forcefields.append(force_field(grav)) # puts gravity back

# do_every is the same as lifetime so it will only delete gravity once
zero_G=[zeroG_commands,zeroG_reset,med_life,med_life,'Zero Gravity']



def black_hole_commands(gamestate):
    del gamestate.forcefields[0]                # deletes regular gravity and replaces it with
    black_hole=force_field(black_hole_grav)     # a gravitational field consistent with a point mass (a black hole)
    gamestate.forcefields.append(force_field(black_hole_grav))
    black_hole_loc=(screenwidth/2,screenheight-100)
    black_hole=sink('circ',(black_hole_loc,12)) # also creates a sink so that a ball will be lost if it falls into the balck hole
    gamestate.sinks.append(black_hole)
    

def black_hole_reset(gamestate):
    del gamestate.forcefields[0]
    gamestate.forcefields.append(force_field(grav))
    del gamestate.sinks[1]

def black_hole_grav(ball):
    b_h_loc=vec((screenwidth/2,screenheight-100))
    displacement=b_h_loc-ball.pos
    distance_factor=1/modsq(displacement)
    return ball.mass*5000000*distance_factor*unitv(displacement)    # the ball will be attracted to the balck hole according to the inverse square law

black_hole=[black_hole_commands,black_hole_reset,short_life,short_life,'Black Hole']
    


def bonus_ball_commands(gamestate):
    # gives the player another ball. It will start in a random position with random velocity
    gamestate.balls.append(ball_obj((uniform(0,screenwidth),uniform(0,screenheight)),(uniform(-randomvel,randomvel),uniform(-randomvel,randomvel))))

# note: there is no reset command and the command only executes once
bonus_ball=[bonus_ball_commands,empty,one_time,one_time,'Bonus Ball']
    


def switch_controls(gamestate):         # reverses which keys control the flippers
    temp=gamestate.flippers[0].key
    gamestate.flippers[0].key=gamestate.flippers[1].key
    gamestate.flippers[1].key=temp

# note: the command to undo the reversal is the same as the original command
reverse=[switch_controls,switch_controls,short_life,short_life,'Reverse']


def super_bounce_commands(gamestate): # makes the ball extra bouncy
    for ball in gamestate.balls:
        ball.bounce=1.5*ball_bounce

def super_bounce_reset(gamestate):
    for ball in gamestate.balls:
        ball.bounce=ball_bounce

super_bounce=[super_bounce_commands,super_bounce_commands,short_life,short_life,'Super Bounce']



# powerups packaged in a list
all_powerups=[wood_stock,zero_G,black_hole,bonus_ball,reverse,super_bounce]
