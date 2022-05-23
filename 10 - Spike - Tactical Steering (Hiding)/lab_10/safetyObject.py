from vector2d import Vector2D
from graphics import egi, KEY
from random import randrange,random
from graphics import EasyGraphics

from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from world import World

class SafetyObject(object):
    def __init__(self,world,radius):
        #self.pos = Vector2D(randrange(world.cx),randrange(world.cy))
        self.world=world
        self.pos = Vector2D(0,0)
        self.radius = radius
    
    def reinit(self,world):
        self.pos = Vector2D(randrange(world.cx),randrange(world.cy))

    def render(self):
        # wnd_pos = Vector2D(100, 100)
        # dir = radians(random()*360)
        # heading = Vector2D(sin(dir), cos(dir))
        # side = heading.perp()
        # wld_pos = self.world.transform_point(wnd_pos, self.pos, heading, side)
        # # draw the wander circle
        # egi.green_pen()
        # circle = egi.circle(wld_pos,50)
        # print("CIRCLE == ",circle)
        # draw the wander target (little circle on the big circle)
        # egi.red_pen()
        # wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
        # wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
        # egi.circle(wld_pos, 3)
        # print("SafetyObejct Render function")
        # graphic = EasyGraphics()
        # print("graphic  == ",graphic)
        # circle = graphic.circle(Vector2D(0,0),80)
        # print("circel == ",circle)
        circle = egi.circle(Vector2D(0,0),80)
        text = egi.text_at_pos(0, 0, "hello u")
        print("text = ",text)
        print("CIRCLE == ",circle)
        egi.green_pen()
        # 
        # print("circle == ",circle)
        # return circle
    # def __init__(self, world=None):
    #     # self.x = randrange(world.cx)
    #     # self.y = randrange(world.cy)
    #     self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
    #     self.color = 'YELLOW'

    # def draw_circle(self,radius):
    #     # egi.white_pen()
    #     # egi.text_at_pos(0, 0, "hello mother funcker")
    #     # fps_display.draw()
    #     egi = EasyGraphics()
    #     print("egi == ",egi)
    #     print("instanciated easy grahics")
    #     # egi.grey_pen()
    #     # # egi.circle(Vector2D(self.x,self.y),radius)
    #     egi.set_pen_color(name=self.color)
    #     egi.set_stroke(2)
    #     print("self.pos === ",self.pos)
    #     circle = egi.circle(self.pos,radius)  
    #     print("circle=", circle)
     