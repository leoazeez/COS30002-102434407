'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from random import random, randrange

class World(object):

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.target = Vector2D(cx / 2, cy / 2)
        self.hunter = None
        self.agents = []
        self.paused = True
        self.show_info = True

        self.separation_param = 70.0
        self.cohesion_param = 0.0
        self.alignment_param = 0.0

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)

    def render(self):
        for agent in self.agents:
            agent.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)

        if self.show_info:
            infotext = ', '.join(set(agent.mode for agent in self.agents))
            egi.white_pen()
            egi.text_at_pos(0, 0, infotext)

    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts


    # def seek(self, target_pos):
    #     ''' move towards target position '''
    #     desired_vel = (target_pos - self.pos).normalise() * self.max_speed
    #     return (desired_vel - self.vel)

    def separation(self):
        force = Vector2D()
        nbr_agents = len(self.agents)
        if(nbr_agents>2):
            #starting from 1 so we don't include the first agent
            for i in range(1,nbr_agents-1,2):
                self.agents[i].flee(self.agents[i+1].pos, self.separation_param)
            #for the last agent
            self.agents[nbr_agents-1].flee(self.agents[nbr_agents-2].pos, self.separation_param)

        return force

       

    def cohesion(self):
        cohesion = Vector2D()
        for agent in self.agents:
            distance_from_target = agent.pos-self.target
            cohesion += distance_from_target
          
        self.cohesion_param = 100-abs(cohesion.x/len(self.agents)+cohesion.y/len(self.agents))/2
        

        #make the agents go towards the world's target if it exists, otherwise make them
        #sees the center of the world
        # master_agent = None
        # force=Vector2D()
        # #searching for master_agent
        # for agent in self.agents:
        #     if agent.is_master_agent:
        #         master_agent = agent

        # if self.target:
        #     for ag in self.agents:
        #         #force.append(ag.seek(self.target))
        #         print("agent{} is seekign target".format(ag))
        #         force += ag.seek(self.target)
        # else:
        #     target = Vector2D(self.cx/2,self.cy/2)
        #     for ag in self.agents:
        #         force.append(ag.seek(target))
    
        # return force
      
    def alignment(self):
        
        return Vector2D()

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        ''' Transform the given single point, using the provided position,
        and direction (forward and side unit vectors), to object world space. '''
        # make a copy of the original point (so we don't trash it)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)
        # done
        return wld_pt