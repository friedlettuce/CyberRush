import pygame, os

#Generic Enemy Class For Enemies To Utilize
class Enemy(object):
	
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.pathX = [x, end]
		self.pathY = [y, end]
		self.movement = 0
		self.vel = 0
	
	#Function For An Enemy To Move Side To Side On The X Axis
	def move_AlongX(self):
		# If Velocity > 0, Enemy Is Moving To The Right
		if self.vel > 0:
			if self.x < self.pathX[1] + self.vel:
				self.x = self.x + self.vel
			else:
				self.vel = self.vel * -1
				self.x = self.x + self.vel
				self.movement = 0
				
		# If Velocity < 0, Enemy Is Moving To The Left
		elif self.vel < 0:
			if self.x > self.pathX[0] - self.vel:
				self.x = self.x + self.vel
			else:
				self.vel = self.vel * -1
				self.x = self.x + self.vel
				self.movement = 0
	
	#Function For An Enemy To Move Side To Side On The Y Axis
	def move_AlongY(self):
		# If Velocity > 0, Enemy Is Moving Down
		if self.vel > 0:
			if self.y < self.pathY[1] + self.vel:
				self.y = self.y + self.vel
			else:
				self.vel = self.vel * -1
				self.y = self.y + self.vel
				self.movement = 0
				
		# If Velocity < 0, Enemy Is Moving Up
		elif self.vel < 0:
			if self.y > self.pathY[0] - self.vel:
				self.y = self.y + self.vel
			else:
				self.vel = self.vel * -1
				self.y = self.y + self.vel
				self.movement = 0

#Enemy That Will Hover Along X Axis
class HoveringEnemy_X(Enemy):
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.pathX = [x, end]
		self.movement = 0
		self.vel = 5
	
	def draw(self, screen):
		self.move_AlongY()
		
		
	
	