import pygame
import sys
import AICar
import math
import copy
import random
import nnet 
import asyncio


'''KNOWN ISSUES:
Vision lines are not accounting for the size of the car
make maxvision high enough / car size small enough that this does not matter

'''
# globals
START_X = 50
START_Y = 50
X_WIDTH = 2000
Y_WIDTH = 1000
CAR_SIZE = 25
ALLOWED_AREA = 250
MIN_SPEED = 30
TURN_SPEED = 30
VISION_COUNT = 10
VISION_RANGE = 800
NOT_ALLOWED_RECTS = [pygame.Rect((333, 333, 1500, 333))]#,
                     # pygame.Rect((1100, 850, 333, 500)),
                     # pygame.Rect((1100, 0, 333, 150))]
# NNET INSTANCE PARAMETERS
NUM_INPUT = 3 # 3 vision numbers
NUM_HIDDEN = 6 # can change
NUM_OUTPUT = 3 # forwards, left, right

nnet.MUTATION_ARRAY_MIX_PERC = 0.25
PERCENT_TO_BREED = 0.7

# multiple cars
CAR_PARAMS = (VISION_COUNT, VISION_RANGE, 
              (START_X,START_Y), MIN_SPEED, 0)
AICAR_PARAMS = (copy.deepcopy(nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)), *CAR_PARAMS)
VISION_PARAMS = (Y_WIDTH-CAR_SIZE,X_WIDTH-CAR_SIZE,
                 NOT_ALLOWED_RECTS,
                 CAR_SIZE)

NUM_CARS = 500
# PROP_TO_DRAW=0.1



# make car
# raceCar = carsList[0]


# drawing function
def draw(cars, screen):
    screen.fill((0, 0, 0))

    for i in cars:
        pygame.draw.rect(screen, (0, 255, 0), (i.x, i.y, CAR_SIZE, CAR_SIZE))
    pygame.draw.rect(screen, (200, 100, 100), (cars[0].x, cars[0].y, CAR_SIZE, CAR_SIZE))

    for r in NOT_ALLOWED_RECTS:
        pygame.draw.rect(screen, (255,255,0), r)
    # pygame.draw.rect(screen, (255, 255, 0), (ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA))
    

    pygame.display.update()

     



# running func
async def main():
    carsList = []
    aliveList = []
    deceasedList = []
    frameCount=0
    carsList = [AICar.AICar(*AICAR_PARAMS) for i in range(NUM_CARS)]
    # initialize nnets
    for i in carsList:
        i.nnet = nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)

    # randomize starting angles +- 30 degrees
    # for i in carsList:
    #     i.angle = random.random()*60 - 30

        

    aliveList = carsList
    # Initialize pygame
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))

    # Set the background color
    screen.fill((0, 0, 0))

    # make clock
    clock = pygame.time.Clock()
    FPS = 30
    pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   
    # Run the game loop

    while True:
        aliveList[0].selected=True
        frameCount+=1
        # Check for events
        for event in pygame.event.get():
            # Quit if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # remove selected
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    aliveList[0].selected=False
                    aliveList.append(aliveList.pop(0))
                if event.key == pygame.K_RETURN:
                    aliveList[0].selected=False
                    aliveList[0].fitness=0

                    deceasedList.append(aliveList.pop(0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            FPS+=1
            pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

        elif keys[pygame.K_LEFT]:
            FPS-=1
            pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

        if keys[pygame.K_UP]:
            FPS=1000
            pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   
        elif keys[pygame.K_DOWN]:
            FPS=30
            pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

        for i in aliveList:
            if not (i.move((0, 0, X_WIDTH-CAR_SIZE, Y_WIDTH-CAR_SIZE), minSpeed=MIN_SPEED)):
                # TODO update fitness
                # i.fitness=0

                aliveList.remove(i)
                deceasedList.append(i)
                # print(len(aliveList))
                pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   
            # check if it is inside the not allowed region
            for r in NOT_ALLOWED_RECTS:
                if pygame.Rect.colliderect(r,
                                           pygame.Rect(i.x, i.y, CAR_SIZE, CAR_SIZE)):
                    # TODO UPDATE FITNESS
                    # i.fitness=0
                    try:
                        aliveList.remove(i)
                        deceasedList.append(i)
                    except:
                        pass
                    pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

            # # check if it is in the right and bottom half
            # if i.x>X_WIDTH/2 and i.fitness<2:
            #     i.fitness=1
            #     if i.y>Y_WIDTH/2:
            #         i.fitness=2
            # elif i.y>Y_WIDTH/2 and i.fitness<2:
            #     i.fitness=1
            # less strict fitness
            if i.x>START_X+500 or i.y>START_Y+500:
                i.fitness=2
            # purge the ones with 0 fitness
            if frameCount>300 and i.fitness!=2:
                try:
                    aliveList.remove(i)
                    deceasedList.append(i)
                except:
                    pass
                pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

            # if i.getOutput(*VISION_PARAMS)[1] > 0.5:
            #     raceCar.turn(-5)

            # elif i.getOutput(*VISION_PARAMS)[2] > 0.5:
            #     raceCar.turn(5)
            # if i.getOutput(*VISION_PARAMS)[0] > 0.5:
            #     i.speedUp(2)

            if i.getOutput(*VISION_PARAMS)[1] > 0.5:
                i.turn(-TURN_SPEED)

            elif i.getOutput(*VISION_PARAMS)[2] > 0.5:
                i.turn(TURN_SPEED)

        # print('hits (straight,left,right):', raceCar.getVision(*VISION_PARAMS))
        draw(aliveList, screen)
        clock.tick(FPS)
        await asyncio.sleep(0) 
        print(frameCount)
asyncio.run(main()) 
