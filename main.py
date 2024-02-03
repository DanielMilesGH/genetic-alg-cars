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
^^FIXED, collision just checks point. will look weird but works
'''
# globals
START_X = 50
START_Y = 50
START_ANGLE = 90
X_WIDTH = 1800 # screen width
Y_WIDTH = 800 # screen height
CAR_SIZE = 25 # doesn't affect collision, just view
ALLOWED_AREA = 250
MIN_SPEED = 25 # cars can increase their speed
MAX_SPEED = 25 # can't be larger than car_size
TURN_SPEED = 30 
VISION_COUNT = 6 # how high resolution their view is (higher=better)
VISION_RANGE = 500 # how far they can see (divide with vision count for res)
BASIC_MIDDLE = [pygame.Rect((300, 300, 1400, 360))] 
FRAMES_UNTIL_COLLISION_CHECK = 3
# make frames higher checkpoint check lower if cars failing initially
# if high car count, initial fails shouldn't be an issue
FIRST_CHECK_FRAMES = 100
FIRST_CHECKPOINT_CHECK = 8
ADVANCED_OBSTACLES = [pygame.Rect((300, 0, 50, 300)),
                      pygame.Rect((0, 500, 1700, 50)),
                      pygame.Rect((800, 200, 50, 300)),
                      pygame.Rect((1200,0,50,250)),
                      pygame.Rect((800, 200, 50, 500)),
                      pygame.Rect((1500, 200, 300, 50))]
# print(ADVANCED_OBSTACLES[0][0])
# print(ADVANCED_OBSTACLES[0][1])
NOT_ALLOWED_RECTS = ADVANCED_OBSTACLES#,
                    # pygame.Rect((1100, 333, 533, 333))]#,
                     # pygame.Rect((333, 0, 333, 150))]

CHECKPOINTS = [pygame.Rect((300, 300, 2, 200)),
               pygame.Rect((800, 0, 2, 200)),
               pygame.Rect((1200, 250, 2, 250)),
               pygame.Rect((1700, 500, 300, 2)),
               pygame.Rect((1200, 550, 2, 250)),
               pygame.Rect((600, 550, 2, 250))]
# NNET INSTANCE PARAMETERS
NUM_INPUT = 3 # 3 vision numbers
NUM_HIDDEN = 5 # can change 
NUM_OUTPUT = 3 # forwards, left, right

nnet.MUTATION_WEIGHT_MODIFY_CHANCE = 0.15
nnet.MUTATION_ARRAY_MIX_PERC = 0.55
PERCENT_TO_BREED = 0.7

# multiple cars
CAR_PARAMS = (VISION_COUNT, VISION_RANGE, 
              (START_X,START_Y), MIN_SPEED, START_ANGLE)
AICAR_PARAMS = (copy.deepcopy(nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)), *CAR_PARAMS)
VISION_PARAMS = (Y_WIDTH-CAR_SIZE,X_WIDTH-CAR_SIZE,
                 NOT_ALLOWED_RECTS,
                 CAR_SIZE)
NUM_CARS = 700
# PROP_TO_DRAW=0.1



# make car
# raceCar = carsList[0]


# drawing function
def draw(cars, screen, DRAW_THINGS, bestFitness):
    screen.fill((0, 0, 0))
    if not DRAW_THINGS:
        return 0
    for i in cars:
        pygame.draw.rect(screen, (0, 255, 0), (i.x, i.y, CAR_SIZE, CAR_SIZE))
    # first value in aliveList should be the fittest TODO: CHECK?
    pygame.draw.rect(screen, (200, 100, 100), (cars[0].x, cars[0].y, CAR_SIZE, CAR_SIZE))

    for r in NOT_ALLOWED_RECTS:
        pygame.draw.rect(screen, (255,255,0), r)
    # pygame.draw.rect(screen, (255, 255, 0), (ALLOWED_AREA, ALLOWED_AREA, X_WIDTH-2*ALLOWED_AREA, Y_WIDTH-2*ALLOWED_AREA))
    if PHYSICS_CHECK:
        pygame.draw.line(screen, (255,255,255), (cars[0].x+12, cars[0].y+12),
                         (int(cars[0].x + math.cos(math.radians(cars[0].faceAngle)) * 50)+12,
                         int(cars[0].y + math.sin(math.radians(cars[0].faceAngle)) * 50)+12),
                         3)
    for i in CHECKPOINTS:
        pygame.draw.rect(screen, (0,0,255), i)
    text_surface = my_font.render("Curr Best: " + str(bestFitness), False, (255, 255, 255))
    screen.blit(text_surface, (100, 100))

    pygame.display.update()


pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# running func
async def main():
    bestFitness = 0
    BEST_FITNESS = 0
    FITTEST=False
    REGEN = True
    carsList = []
    aliveList = []
    deceasedList = []
    frameCount=0
    carsList = [AICar.AICar(*AICAR_PARAMS) for i in range(NUM_CARS)]
    DRAW_THINGS = True
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

    # main loop
    while True:
        # generation loop
        genLoop = True
        while (genLoop) and len(aliveList)>0:
            # draw the current best

            # aliveList[0].selected=True
            frameCount+=1
            # Check for events
            for event in pygame.event.get():
                # Quit if the user closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # remove selected
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: # select next
                        aliveList[0].selected=False
                        aliveList.append(aliveList.pop(0)) 
                    if event.key == pygame.K_RETURN: # kill current with 0 fitness
                        aliveList[0].selected=False
                        aliveList[0].fitness=0

                        deceasedList.append(aliveList.pop(0))
                    if event.key == pygame.K_ESCAPE: # end current gen
                        genLoop = False
                    if event.key == pygame.K_TAB: # TODO WORK THIS OUT
                        REGEN = False
                    if event.key == pygame.K_SPACE: # stop drawing
                        DRAW_THINGS = not DRAW_THINGS
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                FPS=1000
                pygame.display.set_caption('FPS: ' + str(clock.get_fps()) + ' NumAlive:'+str(len(aliveList)))   
            elif keys[pygame.K_DOWN]:
                FPS=30
                pygame.display.set_caption('FPS: ' + str(clock.get_fps()) + ' NumAlive:'+str(len(aliveList)))   

            draw(aliveList, screen, DRAW_THINGS, bestFitness)
            for i in aliveList:
                i.quadrantCheck(X_WIDTH, Y_WIDTH, X_WIDTH/8)
                # print(i.nnet)
                # print(len(i.quadrants))
                if not (i.move((0, 0, X_WIDTH-CAR_SIZE, Y_WIDTH-CAR_SIZE), minSpeed=MIN_SPEED)):
                    # TODO update fitness
                    # i.fitness=0

                    aliveList.remove(i)
                    deceasedList.append(i)
                    # print(len(aliveList))
                    pygame.display.set_caption('FPS: ' + str(clock.get_fps()) + ' NumAlive:'+str(len(aliveList)))   
                # check if it is inside the not allowed region
                # we only need to check this every 3 frames realistically
                if (frameCount % FRAMES_UNTIL_COLLISION_CHECK):
                    for r in NOT_ALLOWED_RECTS:
                        if pygame.Rect.colliderect(r,
                                                #    pygame.Rect(i.x, i.y, CAR_SIZE, CAR_SIZE)):
                                                pygame.Rect(i.x, i.y, 1, 1)):

                            # TODO UPDATE FITNESS
                            # i.fitness=0
                            try:
                                aliveList.remove(i)
                                deceasedList.append(i)
                            except:
                                pass
                            pygame.display.set_caption('FPS: ' + str(clock.get_fps()) + ' NumAlive:'+str(len(aliveList)))   

                i.checkpointCheck(CHECKPOINTS, CAR_SIZE)
                i.fitnessUpdate()

                # min quadrants * min speed for min fitness
                # if frameCount>300 and i.fitness<(MIN_SPEED * 15):
                #     try:
                #         aliveList.remove(i)
                #         deceasedList.append(i)
                #     except:
                #         pass
                #     pygame.display.set_caption('FPS: ' + str(FPS) + ' NumAlive:'+str(len(aliveList)))   

                if frameCount>FIRST_CHECK_FRAMES and len(i.quadrants) <= FIRST_CHECKPOINT_CHECK:
                    try:
                        aliveList.remove(i)
                        deceasedList.append(i)
                    except:
                        pass
                    pygame.display.set_caption('FPS: ' + str(clock.get_fps()) + ' NumAlive:'+str(len(aliveList)))  
                if i.getOutput(*VISION_PARAMS)[0] > 0.5:
                    i.speedUp(inc=2, maxSpeed=MAX_SPEED)

                if i.getOutput(*VISION_PARAMS)[1] > 0.5:
                    i.turn(-TURN_SPEED)

                elif i.getOutput(*VISION_PARAMS)[2] > 0.5:
                    i.turn(TURN_SPEED)

                # if (len(i.quadrants) > 15) and REGEN:
                if (len(i.checkpointsHit) == len(CHECKPOINTS)) and REGEN:
                    i.fitness=99999
                    genLoop = False
                    break

                # print(len(aliveList))
            # print('hits (straight,left,right):', raceCar.getVision(*VISION_PARAMS))
            clock.tick(FPS)
            await asyncio.sleep(0) 
            if frameCount>500:
                genLoop = False
                break
            # print(frameCount)
        print(frameCount)
        # got out of gen loop, update generation

        # first put everyone in deceased
        for i in range(len(aliveList)):
            deceasedList.append(aliveList.pop())
        for i in deceasedList:
            i.fitnessUpdate()
        deceasedList.sort(reverse=True)
        # print("list of best:", deceasedList[0].checkpointsHit)
        # print("fitness of best:",deceasedList[0].fitness)
        FITTEST = deceasedList[0]
        bestFitness = FITTEST.fitness
        for i in deceasedList:
            i.reset(copy.deepcopy(FITTEST.nnet), *AICAR_PARAMS[1:])  # reset, fitness is saved by the ordering of list


        # # print([i.fitness for i in deceasedList])
        # # TODO, for now getting most fit of all time, instead of top prop
        # if deceasedList[0] > BEST_FITNESS:
        #     fittest=copy.deepcopy(deceasedList[0])

        # BEST_FITNESS = fittest.fitness 
        # fittest.reset()
        # fittest.selected=True
        # for c in deceasedList[0:round(NUM_CARS*PERCENT_TO_BREED)]:
        #     c.reset()
        #     c.nnet.create_mixed_weights(c.nnet, fittest.nnet)

        # for c in deceasedList[round(NUM_CARS*PERCENT_TO_BREED):-1]:
        #     c.reset()
        #     c.nnet.modify_weights()

        '''
        with the following generation updater, take the most fit
        and modify its weights
        '''

        # print(FITTEST.fitness)
        # FITTEST.reset(FITTEST.nnet, *AICAR_PARAMS[1:])
        aliveList.append(FITTEST)
        for c in deceasedList[1:round(NUM_CARS*PERCENT_TO_BREED)]:
            c.nnet.modify_weights()
            # print(c)
            aliveList.append(c)
            # print(c.nnet.printStuff())
            # deceasedList[-1].nnet.modify_weights()
        # print(BEST_FITNESS)
        for c in deceasedList[round(NUM_CARS*PERCENT_TO_BREED):]:
            c.reset(copy.deepcopy(nnet.Nnet(NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT)), 
                    *AICAR_PARAMS[1:])
            aliveList.append(c)

        # print(len(aliveList))
        deceasedList = []
        # print()
        frameCount = 0
# want a way of controlling myself to check physics
def physicsCheck():
    raceCar = AICar.AICar(*AICAR_PARAMS)

    # Initialize pygame
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))

    # Set the background color
    screen.fill((0, 0, 0))

    # make clock
    clock = pygame.time.Clock()
    FPS = 30

    while True:
        # Check for events
        for event in pygame.event.get():
            # Quit if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            raceCar.turn(TURN_SPEED)
        elif keys[pygame.K_LEFT]:
            raceCar.turn(-TURN_SPEED)
        if keys[pygame.K_UP]:
            raceCar.speedUp(inc=2, maxSpeed=MAX_SPEED)
        raceCar.move((0, 0, X_WIDTH-CAR_SIZE, Y_WIDTH-CAR_SIZE), minSpeed=MIN_SPEED) 
        draw([raceCar], screen, True)
        clock.tick(FPS)
        # print('moveAngle:',raceCar.moveAngle)
        # print('faceAngle:',raceCar.faceAngle)
        raceCar.quadrantCheck(X_WIDTH, Y_WIDTH, X_WIDTH/8)
        raceCar.checkpointCheck(CHECKPOINTS, CAR_SIZE)
        print('quadrants:', raceCar.quadrants)
        print('checkpoints:', raceCar.checkpointsHit)

PHYSICS_CHECK=False
if PHYSICS_CHECK:
    physicsCheck()

asyncio.run(main()) 
