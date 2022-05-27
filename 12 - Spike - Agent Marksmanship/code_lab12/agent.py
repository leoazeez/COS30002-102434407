'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from typing_extensions import Self
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from random import uniform
import keyboard #pip3 install keyboard


AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander',
    KEY._9: 'marksmanship',

}

class Agent(object):
    #NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        ### ADD 'normal' and 'fast' speeds here
        'normal': 1.3,
        'fast': 1.7
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass
        self.is_attacker = False
        self.target = None
        self.is_bullet = False
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        ### path to follow?
        self.path = Path()
        self.randomise_path() 
        self.waypoint_threshold = 0.0 

        ### wander details
         # NEW WANDER INFO
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

        # limits?
        self.max_speed = 20.0 * scale
        self.min_speed = 0.5 * scale
        ## max_force ??
        self.max_force = 500.0

        # debug draw info?
        self.show_info = False

    def randomise_path(self):
        cx = self.world.cx # width
        cy = self.world.cy # height
        margin = min(cx, cy) * (1/6) # use this for padding in the next line ...
        #margin_max = max(cx,cy) * (1/6)
        num_pts = 10
        self.path.create_random_path(num_pts, margin, margin, cx, cy)

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            force = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            force = self.flee(self.world.target)
        elif mode == 'pursuit':
            force = self.pursuit(self.world.hunter)
        elif mode == 'wander':
            force = self.wander(delta)
        elif mode == 'follow_path':
            force = self.follow_path()
        elif mode == 'hide':
            force = self.hide()
        elif mode == "marksmanship":
            force = Vector2D()
        
        else:
            force = Vector2D()
        self.force = force
        return force

    def follow_path(self):
        if(self.path.is_finished):
            # If heading to final point (is_finished?)
            # Return a slow down force vector (Arrive)
            arrive = self.arrive(self.path.current_pt(), 'slow')
            return arrive
        else:
            # Else
            # If within threshold distance of current way point, inc to next in path
            # Return a force vector to head to current point at full speed (Seek)
            if(self.pos.distance(self.path.current_pt())<=self.waypoint_threshold):
                self.path.inc_current_pt()
            force_vector = self.seek(self.path.current_pt())
            return force_vector

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        force = self.calculate(delta)
        if not force:
            force = Vector2D(20, 20)

        ## limit force? <-- for wander
        force.truncate(self.max_force) 
        # determin the new accelteration
        # print("x_force = ",force.x)
        # print("x_accel = ",self.accel.x)
        self.accel.x = force.x / self.mass  # not needed if mass = 1.0
        self.accel.y = force.y / self.mass
        # new velocity
        self.vel += self.accel * delta
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
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()

        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        # draw wander info?
        if self.mode == 'wander':
            # calculate the center of the wander circle in front of the agent
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)

        if self.mode == 'hide':
            from random import randint
            egi.green_pen()
            x = randint(0,200)
            y = randint(0,200)
            egi.circle(Vector2D(450,450),45)
           

        if self.mode == 'marksmanship':
            if self.is_attacker:
                self.pos = Vector2D(150,400)
                self.setHeading()
      

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            if not self.force:
                self.force = Vector2D(20,20)
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

      
        self.world.target = Vector2D() #To hide the World's target (the red cross)
        for agent in self.world.agents:
            if agent.is_bullet and self.target :
                dist = (self.target.pos - agent.pos).length()
                if dist < 55:
                    agent.color = "AQUA"
                    agent.vehicle_shape = [
                    Point2D(-1.0,  0.4),
                    Point2D( 0.5,  0.0),
                    Point2D(-1.0, -0.4)]
                    self.world.agents.remove(agent)
                    break
              

    def setHeading(self):
        if self.is_attacker and self.target:        
            self.color = "RED"
            target_vel = self.target.vel
            self.target.pos.x = self.pos.y
            self.vel = target_vel
    

    def hitWithRrifle(self,target):
        desired_vel = (target.pos - self.pos).normalise() * (self.max_speed/5)
        return (desired_vel - self.vel)  

    def hitWithRocket(self,target):
        desired_vel = (target.pos - self.pos).normalise() * (self.max_speed/100)
        return (desired_vel - self.vel)  

    def hitWithGun(self,target):
        radius = 70
        position = Vector2D(randrange(int(target.pos.x-radius),int(target.pos.x+radius)), 
        randrange(int(target.pos.y-radius),int(target.pos.y+radius)))
        desired_vel = (position - self.pos).normalise() * (self.max_speed/5)
        return (desired_vel - self.vel)

    def hitWithGrenade(self,target):
        radius = 70
        position = Vector2D(randrange(int(target.pos.x-radius),int(target.pos.x+radius)), 
        randrange(int(target.pos.y-radius),int(target.pos.y+radius)))
        desired_vel = (position - self.pos).normalise() * (self.max_speed/100)
        return (desired_vel - self.vel)

    def shoot_target(self,weapon):
        if self.mode == 'marksmanship' and weapon == 'rifle':
            print("rifle")
            bullet = Agent(self.world)
            bullet.is_bullet = True
            bullet.color = "WHITE"
            bullet.vehicle_shape = [
            Point2D(-1.0,  0.2),
            Point2D( 0,  0.0),
            Point2D(-1.0, -0.2)]
            bullet.pos = self.pos
            self.world.agents.append(bullet)
            bullet.hitWithRrifle(self.target)
            #bullet.arrive(self.target.pos,self.max_speed)
                     

        elif self.mode == 'marksmanship' and weapon == 'rocket':
            print("rocket")
            bullet = Agent(self.world)
            bullet.is_bullet = True
            bullet.color = "BLUE"
            bullet.vehicle_shape = [
            Point2D(-1.0,  0.2),
            Point2D( 0,  0.0),
            Point2D(-1.0, -0.2)]
            bullet.pos = self.pos
            self.world.agents.append(bullet)
            bullet.hitWithRocket(self.target)

        elif self.mode == 'marksmanship' and weapon == 'gun':
            print("Gun")
            bullet = Agent(self.world)
            bullet.is_bullet = True
            bullet.color = "GREY"
            bullet.vehicle_shape = [
            Point2D(-1.0,  0.2),
            Point2D( 0,  0.0),
            Point2D(-1.0, -0.2),Point2D( 0,  0.0)]
            bullet.pos = self.pos
            self.world.agents.append(bullet)
            bullet.hitWithGun(self.target)
        elif self.mode == 'marksmanship' and weapon == 'grenade':
            print("Grenade")
            bullet = Agent(self.world)
            bullet.is_bullet = True
            bullet.color = "GREEN"
            bullet.vehicle_shape = [
            Point2D(-1.0,  0.2),
            Point2D( 0,  0.0),
            Point2D(-1.0, -0.2)]
            bullet.pos = self.pos
            self.world.agents.append(bullet)
            bullet.hitWithGrenade(self.target)
    def drawCircle(self):
        egi.green_pen()
        egi.circle(Vector2D(50,50), 45)
    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        default_panic_destance = 700
        distance_from_hunter = (hunter_pos - self.pos).length()
        print("distance_from_hunter ::",distance_from_hunter)
        if distance_from_hunter < default_panic_destance:
            ## add flee calculations (first)
            desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
            return desired_vel
        else:
            print("Agent is Too Far from the flee location")

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

    def hide(self):
        pass
    def wander(self, delta):
        ''' random wandering using a projected jitter circle '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target) 

