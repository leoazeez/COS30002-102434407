'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games, by Clinton Woodward <cwoodward@swin.edu.au>
For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._9: 'hide',
}


class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':1.5,
        'fast':2.5
        ### ADD 'normal' and 'fast' speeds here
    }

    def __init__(self,world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        # limits?
        self.max_speed = 5000.0
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.safe_area = Vector2D(450,450)
        self.is_prey = False
        #self.acceleration = Vector2D(0,0)

    def calculate(self):
        # reset the steering force
        mode = self.mode
        accel = Vector2D()
        if mode == 'seek':
            accel = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            accel = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            accel = self.flee(self.world.target)
        elif mode == 'pursuit':
            force = self.pursuit(self.world.hunter)
        elif mode == 'hide':
            accel = self.hide(self.world.hunter)
        else:
            accel = Vector2D()
        self.acceleration = accel
        return accel

    def update(self, delta):
        ''' update vehicle position and orientation '''
        acceleration = self.calculate()
        # new velocity
        self.vel += acceleration * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        egi.set_pen_color(name=self.color)
        egi.set_stroke(2)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        if self.mode == 'hide':
            #x = randint(0,200)
            #y = randint(0,200)
            egi.green_pen()
            egi.circle(self.safe_area,45)
            egi.cross(self.safe_area, 7)
            egi.blue_pen()
            egi.circle(Vector2D(250,90), 50)
            egi.cross(Vector2D(250,90), 7)
          
       
    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        default_panic_destance = 700
        distance_from_hunter = (hunter_pos - self.pos).length()
        print("distance_from_hunter ::",distance_from_hunter)
        if distance_from_hunter < default_panic_destance:
            ## add flee calculations (first)
            desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
            return desired_vel
        else:
            print("Agent is Safe")
        return Vector2D()

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''

## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def seek_safety(self):
        target_pos = self.pos
        distance_form_safe_area = (self.safe_area - self.pos).length()
        if distance_form_safe_area > 30:
            target_pos = self.safe_area
            desired_vel = (target_pos - self.pos).normalise() * self.max_speed
            return (desired_vel - self.vel)
        # else:
        #     #self.hide(self.world.hunter)
        #     self.stop()
     
        
    def stop(self):
        accel = self.arrive(self.safe_area, 'slow')
        return accel
       

    def hide(self,hunter):
        if self.is_prey:
            default_panic_destance = 70
            if not hunter:
                #default value that is > panic distance, to indicate that the hunetr is far from the agent
                distance_from_hunter = 100 
            else:
                distance_from_hunter = (hunter.pos - self.pos).length()

            if distance_from_hunter < default_panic_destance:
                print("hunter is too close.. seek safety")
                self.seek_safety()

            else:
                print("agent is safe seeking target")
                self.seek(self.world.target)
        
        else:
            target_pos = Vector2D(randrange(self.world.cx), randrange(self.world.cy))
            self.seek(target_pos)
      
        return Vector2D()
        # else:
        #     print("agent is safe seeking target")
        #     target = Vector2D(200,200)
        #     target = hunter_pos
        #     desired_vel = (target - self.pos).normalise() * self.max_speed
        #     return (desired_vel - self.vel)
        #     return self.seek(target)#(self.world.target)
        # distance_from_safe_area = (self.safe_area - self.pos).length()
        # if distance_from_safe_area > 35:
         
        # else:
        #     target_pos = self.pos
        #     desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        #     return (desired_vel - self.vel)
        # # desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        # # target_pos = self.pos#safe_area
        # desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        # return (desired_vel - self.vel)
        # print("Hiding")
        
        # desired_vel = (self.safe_area - self.pos)#.normalise() * self.max_speed
        # return (desired_vel - self.vel)
        # print("distance from safe area =",distance_from_safe_area)
        # accel = self.seek(self.safe_area)
        # return accel
        # if distance_from_safe_area > 35:
        #     print("seeking target")
        #     accel = self.seek(self.safe_area)
        #     return accel
        #     return self.seek(self.world.target)
        #     #desired_vel = self.vel
        #     #return self.pos
        #     #return self.seek(self.pos)
        #     #print("arriving")
        #    # return self.arrive(self.pos,"fast")
        # else:
        #     #print("seeking safety")
        #     #seek =self.safe_area
        #     print("seeking safe area")
        #     accel = self.seek(self.safe_area)
        #     return accel
        #     return self.arrive(self.safe_area,"slow")
        # #return self.seek(seek)
            
        
        # print("hide function")
        # print("self.pos == ", self.pos)
        # print("safe area",self.safe_area)
        # self.seek(self.safe_area)
        # #desired_vel = (self.safe_area-self.pos).normalise() * self.max_speed
        # distance_from_safe_area = (self.safe_area - self.pos).length()
        # print("distance == ",distance_from_safe_area)
        # if distance_from_safe_area < 20:
        #     #desired_vel = self.vel
        #     self.seek(self.pos)

        # return (desired_vel - self.vel)
        
  
        #   desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        # return (desired_vel - self.vel)

