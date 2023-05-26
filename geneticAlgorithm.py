import pygame
import sys
import AICar
import math
import copy
import random
import nnet 


'''KNOWN ISSUES:
Vision lines are not accounting for the size of the car
make maxvision high enough / car size small enough that this does not matter

getVision only assumes one not allowed rect exists, can change later

'''
# globals
START_X = 100
START_Y = 100
X_WIDTH = 2000
Y_WIDTH = 1000
CAR_SIZE = 20
ALLOWED_AREA = 300
MIN_SPEED = 10



# NNET INSTANCE PARAMETERS
NUM_INPUT = 3 # 3 vision numbers
NUM_HIDDEN = 3 # can change
NUM_OUTPUT = 3 # forwards, left, right

nnet.MUTATION_ARRAY_MIX_PERC = 0.25
PERCENT_TO_BREED = 0.7

# multiple cars
CAR_PARAMS = (10, 1000, 
              (START_X,START_Y), MIN_SPEED, 0)
AICAR_PARAMS = (copy.deepcopy(nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)), *CAR_PARAMS)
VISION_PARAMS = (Y_WIDTH-CAR_SIZE,X_WIDTH-CAR_SIZE,
                 pygame.Rect((ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA)),
                 CAR_SIZE)

NUM_CARS = 50
PERCENT_TO_DRAW=1

carsList = []
aliveList = []
deceasedList = []

carsList = [AICar.AICar(*AICAR_PARAMS) for i in range(NUM_CARS)]
# initialize nnets
for i in carsList:
    i.nnet = nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)
# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))

# Set the background color
screen.fill((0, 0, 0))

# make clock
clock = pygame.time.Clock()

# make car
# raceCar = carsList[0]



# drawing function
def draw(cars):
    screen.fill((0, 0, 0))
    for i in cars:
        pygame.draw.rect(screen, (0, 255, 0), (i.x, i.y, CAR_SIZE, CAR_SIZE))
    pygame.draw.rect(screen, (255, 255, 0), (ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA))
    

    pygame.display.update()

# randomize starting angles +- 30 degrees
for i in carsList:
    i.angle = random.random()*60 - 30


aliveList = carsList
FPS = 30
pygame.display.set_caption(str(FPS))        

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
        FPS+=1
        pygame.display.set_caption(str(FPS))        

    elif keys[pygame.K_LEFT]:
        FPS-=1
        pygame.display.set_caption(str(FPS))        

    if keys[pygame.K_UP]:
        FPS=1000
        pygame.display.set_caption(str(FPS))        
    elif keys[pygame.K_DOWN]:
        FPS=30
        pygame.display.set_caption(str(FPS)) 
    for i in aliveList:
        if not (i.move((0, 0, X_WIDTH-CAR_SIZE, Y_WIDTH-CAR_SIZE), minSpeed=MIN_SPEED)):
            # TODO update fitness
            i.fitness=0

            aliveList.remove(i)
            deceasedList.append(i)
        # check if it is inside the not allowed region
        if pygame.Rect.colliderect(pygame.Rect(ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA),
                                   pygame.Rect(i.x, i.y, CAR_SIZE, CAR_SIZE)):
            # TODO UPDATE FITNESS
            i.fitness=0
            aliveList.remove(i)
            deceasedList.append(i)

        # if i.getOutput(*VISION_PARAMS)[0] > 0.5:
        #     raceCar.speedUp(2)

        # if i.getOutput(*VISION_PARAMS)[1] > 0.5:
        #     raceCar.turn(-5)

        # elif i.getOutput(*VISION_PARAMS)[2] > 0.5:
        #     raceCar.turn(5)
        if i.getOutput(*VISION_PARAMS)[1] > 0.5:
            i.turn(-5)

        elif i.getOutput(*VISION_PARAMS)[2] > 0.5:
            i.turn(5)

    # print('hits (straight,left,right):', raceCar.getVision(*VISION_PARAMS))
    print(len(aliveList))
    draw(aliveList)
    clock.tick(FPS)