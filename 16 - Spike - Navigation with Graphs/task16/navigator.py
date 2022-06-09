from point2d import Point2D

class Navigator(object):
    def __init__(self, pos_x,pos_y,box_list):
        self.pos = Point2D(pos_x,pos_y)
        self.path = []
        self.radius = 10
        self.end = False 
        self.box_list = box_list

    def current_pos(self):
        return self.pos
        
  
    def update(self):   
        if self.path:
            source = self.pos
            target = self.box_list[self.path[0]]._vc
            
            self.pos.x += target.x - source.x
            self.pos.y += target.y - source.y
            print("New pos ===",self.pos)
            self.path.pop(0)

        else:
            self.end = True
            print("End of path")        


