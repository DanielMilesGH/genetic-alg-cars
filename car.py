import math
class Car():
    def __init__(self, loc, startSpeed, startAngle):
        self.x = loc[0]
        self.y = loc[1]
        self.speed = startSpeed
        self.angle = startAngle
    
    def move(self, bounds, minSpeed):
        # move x based on cos            
        self.x += math.cos(math.radians(self.angle)) * self.speed
        
        # move y based on sin
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # every time you move, account for friction
        if self.speed>minSpeed:
            self.speed-=1
        
        # check if went over bounds, if did, set location to the bound, return False
        if self.x<bounds[0]:
            self.x=bounds[0]
            return False
        elif self.x>bounds[2]:
            self.x=bounds[2]
            return False

        if self.y<bounds[1]:
            self.y=bounds[1]
            return False

        elif self.y>bounds[3]:
            self.y=bounds[3]
            return False

        return True
        
    def speedUp(self, inc):
        self.speed+=inc

    def turn(self, angle):
    	self.angle+=angle
    	self.angle%=360
if __name__ == '__main__':
    print('test')
    