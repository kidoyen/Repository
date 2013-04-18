from math import e, pi, cos, sin, sqrt, atan
from pygame import *


FPS=40                      # Frames per second game will run at

screenwidth=500
screenheight=850
dt_strd=1/float(FPS)        # time constant used in physics calculations

halfsinkwidth=80            # spacing of gap at bottom of screen (half this quantity is more convenient to work with)
randompos=50                # magnitude of randomness when choosing a random position
randomvel=300               # magnitude of randomness when choosing a random velocity

outline_thickness=1         # outline ball and flippers with 1 pixel of black
outline_color=(0,0,0)       



# vector class converts a tuple into a vector with its head at the location of the tuple and tail at the origin
# used to keep track of position, velocity, acceleration, and used for collision detection

class vec(tuple):           
    def __add__(self,other):
        return vec(x+y for x, y in zip(self,other))
    def __mul__(self,c):
        return vec(x*c for x in self)
    def __rmul__(self,c):
        return vec(x*c for x in self)
    def __sub__(self,other):
        return vec(x-y for x, y in zip(self,other))
    def tup(self):                                      # returns contents in tuple format
        return (self[0],self[1])
    def rtup(self):                                     # rtup rounds the values to whole numbers first for display purposes
        return (int(round(self[0])),int(round(self[1])))


def modulus(vec):                                       # length of vector
    return sqrt(vec[0]**2+vec[1]**2)

def modsq(vec):                                         # square of length of vector
    return (vec[0]**2+vec[1]**2)

def dist_between(first,second):                         # distance between two vectors
    return modulus(first-second)

def unitv(angle_or_vec):                # returns unit vector in direction of input vector or input angle
    if type(angle_or_vec)==float:
        return vec((cos(angle_or_vec),sin(angle_or_vec)))
    else:
        return angle_or_vec*(1/modulus(angle_or_vec))

def dot(self,other):                    # dot product
    return (self[0]*other[0]+self[1]*other[1])

def cross(self,other):                  # signed magnitude of cross product (using right hand rule)
    return(self[0]*other[1]-self[1]*other[0])

def unitperp(vector):                   # returns normalized vector perpendicular to input (using right hand rule)
    return unitv(vec((-vector[1],vector[0])))


# ball constants
ball_rad=10
ball_mass=10
ball_charge=0
ball_bounce=0.7
ball_color=(155,155,155)


# ball class
class ball_obj:
    def __init__(self,position,velocity,color=ball_color,radius=ball_rad,mass=ball_mass,charge=ball_charge,bounce=ball_bounce):
        self.pos=vec(position)              # position and velocity described with vectors
        self.vel=vec(velocity)
        self.col=color
        self.rad=radius                     # how wide the balls will be drawn
        self.mass=mass                      # mass of the ball
        self.charge=charge                  # electric charge of the ball
        self.bounce=bounce                  # describes how much velocity is preserved during collision


# forcefield class holds a function that accepts the state of the game as input
# and outputs the vector acceleration experienced by the ball
class force_field():
    def __init__(self,function):
        self.force=function

def grav(gamestate):                        # default gravity makes all objects accelerate at the same rate
    g=500
    return vec((0,g))



# border constants
borwi=20                                    # how wide to draw the borders
bordercolor=(0,0,255)                       # borders will be blue


# border class to define the objects that will serve as boundaries to the game
class Border():
    def __init__(self,shape='rect',vertices=(),collision_info=[]):
        self.shape=shape                    # default shape is a rectangle but other polygons can be implemented
        self.vertices=vertices              # tuple holding tuples describing the location of vertices
        self.col=bordercolor
        self.collision_info=collision_info  # holds vectors describing the actual collision surfaces (more about this later in collision detection part)

# function that creates a list containing the default borders at the start of the game
def initializeBorder(borwi=borwi):
        output=[]

        vertices=((0,0),(borwi,screenheight))                       # only two points needed to define a rectangle in pygame
        collision_for_left=[[vec((borwi,0)),vec((0,screenheight))]]
        leftside=Border('rect',vertices,collision_for_left)         # this will be the vertical border on the left of the screen
        output.append(leftside)

        vertices=((screenwidth-borwi,0),(screenwidth,screenheight))
        collision_for_right=[[vec((screenwidth-borwi,screenheight)),vec((0,-screenheight))]]
        rightside=Border('rect',vertices,collision_for_right)       # border on the right
        output.append(rightside)

        vertices=((0,0),(screenwidth,borwi))
        collision_for_top=[[vec((screenwidth,borwi)),vec((-screenwidth,0))]]
        topside=Border('rect',vertices,collision_for_top)           # border on the ceiling
        output.append(topside)

        vertices=((0,screenheight-borwi),(screenwidth,screenheight))
        collision_for_bottom=[[vec((0,screenheight-borwi)),vec((screenwidth,0))]]
        bottomside=Border('rect',vertices,collision_for_bottom)     # border on the bottom that was useful for early debugging
        output.append(bottomside)                                  # but is no longer needed due to the sink at the bottom of the screen
        


        bottom_left_corner=(0,screenheight)                         # define the vertices of the left slope
        bottom_right_corner=(int(screenwidth/2)-halfsinkwidth,screenheight)
        top_corner=(0,int(screenheight/2))

        vertices=(bottom_left_corner,bottom_right_corner,top_corner)
        collision_for_left_slope=[[vec(top_corner),vec((int(screenwidth/2)-halfsinkwidth,int(screenheight/2)))]]
        leftslope=Border('tri',vertices,collision_for_left_slope)   # slopes are triangles
        #output.append(leftslope)


        bottom_right_corner=(screenwidth,screenheight)              # vertices of right slope
        bottom_left_corner=(int(screenwidth/2)+halfsinkwidth,screenheight)
        top_corner=(screenwidth,int(screenheight/2))

        vertices=(bottom_right_corner,bottom_left_corner,top_corner)
        collision_for_right_slope=[[vec(bottom_left_corner),vec((int(screenwidth/2)-halfsinkwidth,-int(screenheight/2)))]]
        rightslope=Border('tri',vertices,collision_for_right_slope)
        #output.append(rightslope)

        return output


# function to detect and resolve collisions between one border and one ball
def collision_detect_resolve(border,ball):
    if border.collision_info:                                       # first checks to see that collision information is defined
        
        for bord_location in border.collision_info:                 # loops over all the sets of data for collision. All the borders in this version are effectively half-planes
                                                                    # and so only need one set of data, but the capability for multifaced surfaces is there
                                                                    
            ball_rel_pos=ball.pos-bord_location[0]                  # first vector in list is the actual location of the border so the position of the ball relative
                                                                    # to the border can be calculated
                                                                    
            bord_rel_pos=bord_location[1]                           # second vector in the list holds the border surface
            
            dist=cross(ball_rel_pos,bord_rel_pos)/modulus(bord_rel_pos)-ball.rad        # the cross product essentially calculated the distance between the center of the ball
                                                                                        # and the ray containing the surface, along the perpendicular. Then the radius of the ball is factored in
                                                                                        # to correct for the treatment of the ball as a point
            if dist<0:
                parallel_comp=dot(bord_rel_pos,ball_rel_pos)/modsq(bord_rel_pos)        # the distance being negative doesn't necessarily indicate a collision
                if parallel_comp>0 and parallel_comp<1:                                 # this dot product calculates how far the ball is parallel to the surface,
                                                                                        # if this quantity is >0 or <1 then there is a collision
                                                                                        
                    direction=unitperp(bord_rel_pos)                                    # this is the direction of the "force" applied by the border.
                    ball.pos+=direction*dist                                            # the position of the ball is offset so that it is no longer intersecting the border.
                    new_vel=ball.vel-2*direction*dot(ball.vel,direction)*ball.bounce    # the velocity of the ball is offset such that the component perpendicular to the border
                    ball.vel=new_vel                                                    # is reversed, but is slower than before due to energy dissipation
                    

# creates a range of floats from initial to final (inclusive), with number of elements equal to length
def my_range(initial,end,length):
    output=[]
    increment=float((end-initial))/(length-1)
    for i in range(length):
        output.append(initial+i*increment)
    return output


# flipper constants
flipper_increment=pi/10             # how much to rotate the flipper per update
flippercolor=(155,155,155)
axis_rad=20                         # radius of the circle surrounding where the flipper pivots
end_rad=11                          # radius of the circle at the end of the flipper
f_length=120                        # length from center of axis circle to center of end circle
num_increments=6                    # how many different angles the flippers can have
extra_bounce=1.2                    # how much extra bounce to impart (otherwise the ball would always lose energy from collisions from walls)


# flippers used to hit the ball (see drawing on design documents)
class flipper():
    def __init__(self,axis_pos,axis_rad,length=f_length,end_rad=end_rad,angle_range=[0],key=None):
        self.axis_pos=axis_pos      # vector describing center of the axis circle
        self.axis_rad=axis_rad
        self.length=length
        self.end_rad=end_rad
        self.angle_index=0          # describes the angle the flipper is at from the list of angles in range
        self.range=angle_range
        self.key=key                # key to press to move flipper
        self.alpha=atan(float(axis_rad-end_rad)/length)     # describes slope between surface tangent to circles and the line connecting the centers of the circles
        

# function that creates a list of default flippers at the start of the game
def initializeFlippers():
    output=[]
    left_axis=vec((screenwidth/3-halfsinkwidth,screenheight*3/4))
    left_range=my_range(pi/8,-pi/8,num_increments)          # max angle will be 45 degrees relative to the horizontal and the resting angle is -45 degrees
    left_key=K_v                                            # use the K key to control this flipper
    leftflipper=flipper(left_axis,axis_rad,f_length,end_rad,left_range,left_key)
    output.append(leftflipper)


    right_axis=vec((screenwidth*2/3+halfsinkwidth,screenheight*3/4))
    right_range=my_range(-pi/8,pi/8,num_increments)         # range is reversed because right flipper has opposite orientation than left flipper
    right_key=K_m
    rightflipper=flipper(right_axis,axis_rad,-f_length,end_rad,right_range,right_key) # length is made negative for the same reason
    output.append(rightflipper)
    
    return output

# updates position of flipper
def update_flipper(flipper, keys_down):
        if keys_down[flipper.key]:                          # if the correct key is pressed
            if flipper.angle_index<num_increments-1:        # and the angle isn't at its maximum
                flipper.angle_index+=1                      # the flipper will rotate upwards.
        elif  flipper.angle_index>0:                        # if the key is not pressed and the angle isn't at its maximimum
            flipper.angle_index-=1                          # the flipper will rotate back downwards.


# this function handles the math to accurately draw the flipper
def draw_flipper(flipper,screen):

    axis_pos=flipper.axis_pos
    angle=flipper.range[flipper.angle_index]
    end_pos=axis_pos+flipper.length*unitv(angle)

    axis_offset=flipper.axis_rad*unitv(angle+pi/2)

    axis_topvert=axis_pos+axis_offset
    axis_bottomvert=axis_pos-axis_offset

    end_offset=flipper.end_rad*unitv(angle+pi/2)

    end_topvert=end_pos-end_offset
    end_bottomvert=end_pos+end_offset

    vertices=(axis_topvert.rtup(),axis_bottomvert.rtup(),end_topvert.rtup(),end_bottomvert.rtup())      # describes the non-circle body of the flipper


    draw.polygon(screen,flippercolor,vertices)                              # draws body
    draw.polygon(screen,outline_color,vertices,outline_thickness)           # and outlines it.
    draw.circle(screen,flippercolor,axis_pos.rtup(),flipper.axis_rad)       # draws axis circle
    draw.circle(screen,outline_color,axis_pos.rtup(),flipper.axis_rad,outline_thickness)
    draw.circle(screen,flippercolor,end_pos.rtup(),flipper.end_rad)         # draws end circle
    draw.circle(screen,outline_color,end_pos.rtup(),flipper.end_rad,outline_thickness)


# handles the collisions between a ball and a flipper
def collision_flipper(flipper,ball):                                        # uses similar method as the borders
    angle=flipper.range[flipper.angle_index]
    top_displacement=flipper.axis_pos+flipper.axis_rad*unitv(angle+pi/2)
    bottom_displacement=flipper.axis_pos+flipper.axis_rad*unitv(angle-pi/2)
    top_surface=flipper.length*unitv(angle-flipper.alpha)
    bottom_surface=flipper.length*unitv(angle+flipper.alpha)
    
    ball_rel_pos=ball.pos-top_displacement
    
    dist=cross(ball_rel_pos,top_surface)/modulus(top_surface)-ball.rad
    if dist<0 and dist>2*flipper.end_rad:                                   # gives the top of the flipper some width
        parallel_comp=dot(top_surface,ball_rel_pos)/modsq(top_surface)
        if parallel_comp>0 and parallel_comp<1:
            direction=unitperp(top_surface)
            ball.pos+=direction*dist
            new_vel=ball.vel-2*direction*dot(ball.vel,direction)*(extra_bounce+ball.bounce+abs(dist)/15)*0.5        # gives the ball some extra velocity, incorporating extra bounce,
            ball.vel=new_vel                                                                                        # regular bounce, and the distance of intersection


    ball_rel_pos=ball.pos-bottom_displacement
    dist=cross(ball_rel_pos,bottom_surface)/modulus(bottom_surface)
    if abs(dist)<ball.rad:                                                  # bottom of the flipper is considered as a thin line
        parallel_comp=dot(bottom_surface,ball_rel_pos)/modsq(bottom_surface)
        if parallel_comp>0 and parallel_comp<1:
            direction=unitperp(bottom_surface)
            ball.pos+=direction*dist
            new_vel=ball.vel-2*direction*dot(ball.vel,direction)*(extra_bounce+ball.bounce+abs(dist)/15)*0.5
            ball.vel=new_vel

    axis_to_ball=flipper.axis_pos-ball.pos
    distance=modulus(axis_to_ball)-ball.rad-flipper.axis_rad
    
    if distance<0:
        direction=unitv(axis_to_ball)
        ball.pos+=direction*distance
        new_vel=ball.vel-direction*dot(ball.vel,direction)*(extra_bounce+ball.bounce)
        ball.vel=new_vel

    end_to_ball=flipper.axis_pos+flipper.length*unitv(angle)-ball.pos
    distance=modulus(end_to_ball)-ball.rad-flipper.end_rad

    if distance<0:
        direction=unitv(axis_to_ball)
        ball.pos+=direction*distance
        new_vel=ball.vel-direction*dot(ball.vel,direction)*(extra_bounce+ball.bounce)
        ball.vel=new_vel


# if the ball enters a "sink" object, it will be lost
class sink():
    def __init__(self,shape='rect',location=(0,screenheight-borwi,screenwidth,screenheight),color=(0,0,0)):
        self.shape=shape                                                    # shape supports rectangles and circles
        self.dimensions= (shape!='rect') and location or Rect(location)     # dimensions will be handled depending on if it is a rectangle or not
        self.color=color

    # method which checks if the ball is inside the sink
    def is_in_sink(self,ball):
        if self.shape=='rect':
            return self.dimensions.collidepoint(ball.pos.rtup())            # checks if the center of the ball is inside the rectangle
        if self.shape=='circ':
            return modulus(ball.pos-self.dimensions[0])<self.dimensions[1]  # checks if the center of the ball is inside the circle
        else:
            return False                                                    # other shapes not supported yet
                    
# initializes the default sink at the bottom of the screen
def initializeSinks():
    output=[]
    bottom_sink=sink(location=(0,screenheight-2*borwi,screenwidth,screenheight))
    output.append(bottom_sink)
    return output

# checks to see if a given ball is in any of the sinks, if so it returns True
def remove_ball(ball,sinks):
    for sink in sinks:
        if sink.is_in_sink(ball):
            return True
    return False



