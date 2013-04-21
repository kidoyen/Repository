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
    def __rmul__(self,c):
        return vector(c*self.x,c*self.y)
    def __mul__(self,c):
        return vector(c*self.x,c*self.y)
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
def angrad(angle,radius=1):
    return vector(radius*cos(angle),radius*sin(angle))


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

    def infl(self,rad):
        offset=rad*self.relvec().unitperp()
        return vlist(self.tail-offset,self.head-offset)
        

    def borect(self,rad=0):
        xlist=[self.tail.x,self.head.x]
        ylist=[self.tail.y,self.head.y]
        xmin=min(xlist)-rad
        xmax=max(xlist)+rad
        ymin=min(ylist)-rad
        ymax=max(ylist)+rad
        return rect((xmin,ymin),(xmax,ymax))


def rect(vert1,vert2):
    left=min(vert1[0],vert2[0])
    top=min(vert1[1],vert2[1])
    width=abs(vert1[0]-vert2[0])
    height=abs(vert1[1]-vert2[1])
    return pygame.Rect(left,top,width,height)
    



#BAll CONSTANTS
B_RAD=10                #radius
B_MAS=1                 #mass
B_FORE=(160,160,160)    #main color
B_OUTL=(0,0,0)          #outline color
B_GLIN=(205,205,205)    #glint color
B_GLIR=0.2              #glint radius
B_FRI=1                 #friction
B_BOU=1                 #bounciness

class ball:
    def __init__(self,position,velocity,acceleration=vector(0,0),angle=-pi/4,spin=0,aspin=0,radius=B_RAD,mass=B_MAS,charge=0,friction=B_FRI,bounce=B_BOU,color=B_FORE,outline=B_OUTL):
        self.pos=position       #want pos to be vec, check if position is vec or tuple
        self.vel=velocity
        self.acc=acceleration
        
        self.ang=angle
        self.spi=spin
        self.aspi=aspin
        
        self.rad=radius
        self.m=mass
        self.cha=charge
        self.bmu=friction       #ball mu
        self.bspr=bounce        #ball bounciness
        self.col=color
        self.outl=outline

        self.hist=vlist(self.pos,self.pos)


    def draw(self,screen,camera):
        pygame.draw.circle(screen,self.outl,(self.pos+camera.pos).rtup(),self.rad+1)
        pygame.draw.circle(screen,self.col,(self.pos+camera.pos).rtup(),self.rad)

        glipos=self.pos+camera.pos+angrad(self.ang,self.rad*0.7)
        pygame.draw.circle(screen,B_GLIN,glipos.rtup(),int(self.rad*B_GLIR))
   
    def update(self,dt):
        #euler approximation
        self.vel+=self.acc*dt
        self.pos+=self.vel*dt
        self.hist=vlist(self.hist.head,self.pos)

        self.spi+=self.aspi*dt
        self.ang+=self.spi*dt

        self.aspi=0
        self.acc=vector(0,0)
  



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
    def __init__(self,vertlist,color=W_FORE,grip=W_FRI,bounce=W_BOU):
        self.col=color
        self.wmu=grip
        self.wspr=bounce
        self.surf=surf_vert(vertlist)
        self.bbox=box_vert(vertlist)
        pass

    def draw(self,screen,camera):
        plist=[]
        for v in self.surf:
            plist.append((v.head+camera.pos).rtup())
        pygame.draw.polygon(screen,self.col,plist)

#Wall functions go here
def surf_vert(vertlist):
    output=[]
    num=len(vertlist)
    for i in range(num):
        output.append(vlist(vector(vertlist[i]),vector(vertlist[(i+1)%num])))
    return output

def box_vert(vertlist):
    x_list=[tup[0] for tup in vertlist]
    y_list=[tup[1] for tup in vertlist]
    return rect((min(x_list),min(y_list)),(max(x_list),max(y_list)))

#Maybe put field defaults in different file (powerup file?)

class field:
    def __init__(self,fieldfunc):
        self.func=fieldfunc

#Field functions and constants
G=500       #default gravitational acceleration
#G=0
def gravity(balls):
    for b in balls:
        b.acc+=vector(0,G)



#Camera class, uses WWD var from Main
WWD=400
C_INIT=(WWD/2,0)

C_INIT=(0,0)
class camera:
    def __init__(self,initial=C_INIT):
        self.pos=vector(initial)
    def update(self,balls,otherfactors=None):
        #self.pos+=vector(2,0)
        pass


#Initialization function
def initialize(self):
    self.balls=[ball(vector(200,50),vector(0,1000))]
    self.flippers=[]
    self.walls=[]
    self.walls.append(wall([(-100,800),(300,600),(300,500),(-100,500)]))
    #self.walls.append(wall([(100,400),(-100,500),(100,500),(-100,400)]))
    self.fields.append(field(gravity))

    self.cam=camera()


def darc(self):
    for b in self.balls:
        babox=b.hist.borect(b.rad)                   #ball bound box
        histvec=b.hist.relvec()
        rectin=[]                               #rectangle intersections
        for w in self.walls:
            if pygame.Rect.colliderect(w.bbox,babox):
                rectin.append(w)
               

        vectin=[]                   #vector potential intersections
        for w in rectin:
            for side in w.surf:
                s=side.infl(-b.rad)
                vtail=s.tail-b.hist.tail
                vhead=s.head-b.hist.tail
                sides=cross(vtail,histvec)>0 and cross(vhead,histvec)<0
                front=dot(vtail,histvec)>0 or dot(vhead,histvec)>0
                if sides and front:
                    print "Collision"
                    b.vel=vector(b.vel.x,-0.7*b.vel.y)
                    #b.pos+=vector(0,4)
                
                

        
