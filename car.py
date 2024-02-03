import math
class Car():
    def __init__(self, loc, startSpeed, startAngle):
        self.x = loc[0]
        self.y = loc[1]
        self.speed = startSpeed
        self.faceAngle = startAngle
        self.moveAngle = startAngle
        self.accelerating=False
    def move(self, bounds, minSpeed):
        # move x based on cos            
        self.x += math.cos(math.radians(self.moveAngle)) * self.speed
        
        # move y based on sin
        self.y += math.sin(math.radians(self.moveAngle)) * self.speed
        
        # TODO: FIGURE OUT ANGLE STUFF
        self.moveAngle = self.faceAngle
        # if abs(self.moveAngle-self.faceAngle) > 5:
        #     # difference less than 180, so use normal approach
        #     diff = self.moveAngle - self.faceAngle
        #     #if self.moveAngle > self.faceAngle:
        #     self.moveAngle -= 0.09*diff

        # else:
        #     self.moveAngle = self.faceAngle   

        # every time you move, account for friction
        # if self.speed>minSpeed:
            # self.speed-=1
        # updated
        if self.speed>minSpeed and self.accelerating==False:
            if self.speed>minSpeed+3.5:
                self.speed= round(self.speed**0.93, 2)
            else:
                self.speed=minSpeed
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

        self.accelerating=False
        return True
        
    def speedUp(self, inc, maxSpeed):
        self.accelerating=True
        if (self.speed+inc <= maxSpeed):
            self.speed+=inc
            return True
        return False

    def turn(self, angle):
        self.faceAngle+=angle
        self.faceAngle%=360
if __name__ == '__main__':
    print('test')
    