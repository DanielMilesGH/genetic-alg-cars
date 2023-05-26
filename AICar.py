import os
import sys
import car
import math
import pygame

class AICar(car.Car):

	def __init__(self, nnetInput, visionCount, visionMax, loc, startSpeed, startAngle):
		self.fitness=0
		self.nnet = nnetInput
		self.inputsList = []
		self.visionCount = visionCount
		self.visionMax = visionMax

		self.loc = loc
		self.startSpeed = startSpeed
		self.startAngle = startAngle
		super().__init__(loc, startSpeed, startAngle)


	# vision should be straight ahead, straight left, and right right
	# takes an input of height, width, and not allowed Rects of map
	def getVision(self, height, width, notAllowedRects,carSize):
		# first handle height and width, then handle notAllowedRects
		# straight ahead

		straightHits = 0
		straightHitsRects = 0 
		for i in range(1, self.visionCount+1):
			length = self.visionMax / i

			straightX = self.x + math.cos(math.radians(self.angle)) * length
			straightY = self.y + math.sin(math.radians(self.angle)) * length

			if straightX<0:
				straightHits+=1
			elif straightX>width:
				straightHits+=1
			elif straightY<0:
				straightHits+=1
			elif straightY>height:
				straightHits+=1

			# now check with any rectangles
			if notAllowedRects.clipline((self.x, self.y), (straightX, straightY)):
				straightHitsRects+=1

		leftHits = 0
		leftHitsRects=0
		for i in range(1, self.visionCount+1):
			length = self.visionMax / i

			leftX = self.x + math.cos(math.radians(self.angle-90)) * length
			leftY = self.y + math.sin(math.radians(self.angle-90)) * length

			if leftX<0:
				leftHits+=1
			elif leftX>width:
				leftHits+=1
			elif leftY<0:
				leftHits+=1
			elif leftY>height:
				leftHits+=1

			if notAllowedRects.clipline((self.x, self.y), (leftX, leftY)):
				leftHitsRects+=1

		rightHits = 0
		rightHitsRects=0
		for i in range(1, self.visionCount+1):
			length = self.visionMax / i

			rightX = self.x + math.cos(math.radians(self.angle+90)) * length
			rightY = self.y + math.sin(math.radians(self.angle+90)) * length

			if rightX<0:
				rightHits+=1
			elif rightX>width:
				rightHits+=1
			elif rightY<0:
				rightHits+=1
			elif rightY>height:
				rightHits+=1

			if notAllowedRects.clipline((self.x, self.y), (rightX, rightY)):
				rightHitsRects+=1


		return [max(straightHits, straightHitsRects), 
			    max(leftHits, leftHitsRects), 
			    max(rightHits, rightHitsRects)]


	def getOutput(self, height, width, notAllowedRects,carSize):
		return self.nnet.get_max_value(self.getVision(height, width, notAllowedRects,carSize))

	# method of resetting the car, setting back to default
	def reset(self):
		self.fitness=0
		self.x = self.loc[0]
		self.y = self.loc[1]
		self.speed = self.startSpeed
		self.angle = self.startAngle
	# defining less than and greater than for sorting
	# will try to compare with other car, and if not, try to compare as numerical	
	def __lt__(self, other):
		if type(self) == type(other):
			return self.fitness < other.fitness
		else:
			return self.fitness < other
	def __gt__(self, other):
		if type(self) == type(other):
			return self.fitness > other.fitness
		else:
			return self.fitness > other