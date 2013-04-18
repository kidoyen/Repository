from math import pi, cos, sin, sqrt, atan
import pygame


class vector:
    
    __slots__ = ['x', 'y']
    
    def __init__(self,x_or_pair,y=None):
        if y!=None:
            self.x=x_or_pair
            self.y=y
        else:
            self.x=x_or_pair[0]
            self.y=x_or_pair[1]
    def __repr__(self):
        return '(%f,%f)'%(self.x,self.y)
    def __add__(self,other):
        return vector(self.x+other.x,self.y+other.y)
    def __iadd__(self,other):
        return vector(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return vector(self.x-other.x,self.y-other.y)
    def __neg__(self):
        return vector(-self.x,-self.y)
    def __rmul__(c,self):
        return vector(c*self.x,c*self.y)
    def __mul__(self,c):
        return self*c
    def __div__(self,c):
        return vector(self.x/c,self.y/c)

    def modsq(self):
        return dot(self,self)
    def mag(self):
        return sqrt(self.modsq())
    def rtup(self):
        return (int(round(self.x)),int(round(self.y)))
    def norm(self):
        return self/self.mag()
    def unitperp(self):
        return vector(-self.y,self.x).norm()


def dot(self,other):
    return self.x*other.x+self.y*other.y
def cross(self,other):
    return self.x*other.y-self.y*other.x


class vlist:
    def __init__(self,tail_or_pair,head=None):
        if head!=None:
            self.tail=tail_or_pair
            self.head=head
        else:
            self.tail=tail_or_pair[0]
            self.head=tail_or_pair[1]
    def __repr__(self):
        return '['+str(self.tail)+','+str(self.head)+']'

    def relvec(self):
        return self.head-self.tail
    

u=vector(1,2)



#BAll CONSTANTS
B_RAD=10                #radius
B_MAS=1                 #mass
B_FORE=(120,120,120)    #main color
B_OUTL=(0,0,0)          #outline color
B_GLIN=(255,255,255)    #glint color
B_FRI=1                 #friction
B_BOU=1                 #bounciness

class ball:
    def __init__(self,position,velocity,angle=0,spin=0,radius=B_RAD,mass=B_MAS,charge=0,friction=B_FRI,bounce=B_BOU,color=B_FORE,outline=B_OUTL):
        self.pos=position       #want pos to be vec, check if position is vec or tuple
        self.vel=velocity
        self.ang=angle
        self.spi=spin
        self.rad=radius
        self.m=mass
        self.cha=charge
        self.bmu=friction       #ball mu
        self.bspr=bounce        #ball bounciness
        self.col=color
        self.outl=outline

        self.hist=vlist(self.pos,self.pos)


    def draw(self,screen,camera):
        #simple draw commands
        pass
    def update(self,dt):
        #euler approximation
        #update self.hist
        pass



#FLIPPER CONSTANTS
F_LEN=120
F_AXR=20    # axis radius
F_ENR=10    # end radius
F_ANR=(-pi/4,pi/4)  #angle range

class flipper:
    def __init__(self,initialpos,angle_range,key,orientation):
        self.key=key
        self.hand=orientation
        pass

    def draw(self,screen,camera):
        pass
    def update(self): #increment rate?
        pass



#WALL CONSTANTS
W_FORE=(0,0,200)        #default color is blue
W_FRI=1
W_BOU=1


class wall:
    def __init__(self,vertlist,color,grip=W_FRI,bounce=W_BOU):
        self.col=color
        self.wmu=grip
        self.wspr=bounce
        # self.surf=function(vertlist)
        # self.bbox=otherfunction(vertlist)
        pass

    def draw(self,screen,camera):
        #polygon command, use tuple return from self.surf
        pass

#Wall functions go here



#Maybe put field defaults in different file (powerup file?)

class field:
    def __init__(self,fieldfunc):
        self.func=fieldfunc

#Field functions and constants
G=500       #default gravitational acceleration
def gravity(balls):
    for b in balls:
        b.acc+=vector(0,G)
    #return [G]*len(balls)



#Camera class, uses WWD var from Main
WWD=400
C_INIT=(0,WWD/2)
class camera:
    def __init__(self,initial=C_INIT):
        self.pos=vector(initial)
    def update(self,balls,otherfactors=None):
        pass


#Initialization function
def initialize(self):
    self.balls=[]
    self.flippers=[]
    self.walls=[]
    self.fields.append(field(gravity))


    self.cam=camera()


def darc(self):
    #algorithm to detect and resolve ball collisions
    pass
