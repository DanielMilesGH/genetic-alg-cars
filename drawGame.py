import pygame
import sys
import AICar
import math
'''KNOWN ISSUES:
Vision lines are not accounting for the size of the car
make maxvision high enough / car size small enough that this does not matter

getVision only assumes one not allowed rect exists, can change later

'''
# globals
START_X = 0
START_Y = 0
X_WIDTH = 2000
Y_WIDTH = 1000
CAR_SIZE = 20
ALLOWED_AREA = 300
MIN_SPEED = 10

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))

# Set the background color
screen.fill((0, 0, 0))

# make clock
clock = pygame.time.Clock()

# make car
raceCar = AICar.AICar(nnetInput=0, visionCount=10, visionMax=1000, 
					  loc=(START_X,START_Y), startSpeed=MIN_SPEED, startAngle=0)



# drawing function
def draw():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (raceCar.x, raceCar.y, CAR_SIZE, CAR_SIZE))
    pygame.draw.rect(screen, (255, 255, 0), (ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA))
    

    pygame.draw.rect(screen, (255, 255, 255), (raceCar.x+math.cos(math.radians(raceCar.angle)) * 100, 
    										   raceCar.y+math.sin(math.radians(raceCar.angle)) * 100, 
    										   5, 5))
    pygame.draw.rect(screen, (255, 255, 255), (raceCar.x+math.cos(math.radians(raceCar.angle-90)) * 100, 
    										   raceCar.y+math.sin(math.radians(raceCar.angle-90)) * 100, 
    										   5, 5))
    pygame.draw.rect(screen, (255, 255, 255), (raceCar.x+math.cos(math.radians(raceCar.angle+90)) * 100, 
    										   raceCar.y+math.sin(math.radians(raceCar.angle+90)) * 100, 
    										   5, 5))
    pygame.display.update()


x=0
# Run the game loop
while True:
    # Check for events
    for event in pygame.event.get():
        # Quit if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        raceCar.turn(5)
    elif keys[pygame.K_LEFT]:
        raceCar.turn(-5)
    if keys[pygame.K_UP]:
        raceCar.speedUp(2)
        
    raceCar.move((0, 0, X_WIDTH-CAR_SIZE, Y_WIDTH-CAR_SIZE), minSpeed=MIN_SPEED)

    print('speed:',raceCar.speed)
    print('angle:',raceCar.angle)
    print('hits (straight,left,right):', raceCar.getVision(Y_WIDTH-CAR_SIZE,X_WIDTH-CAR_SIZE,
    	                             [pygame.Rect((ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA))],
    								 CAR_SIZE))
    draw()
    clock.tick(20)