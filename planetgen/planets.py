'''
TODO:


1. SPIKES

2. GOAL

3. ZOOM OUT

4. ENEMIES

















'''

import pygame
from pygame import draw,gfxdraw
import sys
import random
import time
import math
from math import pi, sin, cos, atan2
size = width,height = (600,600)

screen = pygame.display.set_mode(size)

def lerp(prevVal,newVal,amnt):
	difference = (newVal-prevVal)
	add = difference*amnt
	if (difference > pi):
		return prevVal+pi*2
	elif(difference < -pi):
		return prevVal-pi*2
	return prevVal+add

cameraRotation = 0
cameraScale = 1
ptime = 1
def rtPoint(p):
	p = [p[0],p[1]]
	s = sin(cameraRotation)
	c = cos(cameraRotation)
	cx, cy = width/2,height/2
	p[0]-=cx
	p[1]-=cy

	xnew = (p[0]*c-p[1]*s)*cameraScale
	ynew = (p[0]*s+p[1]*c)*cameraScale

	p[0] = xnew+cx
	p[1] = ynew+cy

	return p

def rtPoints(a):
	arr = []


	for p in a:
		arr.append(rtPoint(p))
	return arr
'''
class spike(object):
		draw.circle(screen,(255, 205, 130),center,10 )
	"""docstring for spike"""
	def __init__(self):
		
		self.size = size
	def hit(self,playerpos):
		if 
'''

		

class coin(object):
	"""docstring for coin"""
	def __init__(self, x,y):
		self.x = x
		self.y = y

	def draw(self,screen):

		center = rtPoint((self.x,self.y))
		center[0] = int(center[0])
		center[1] = int(center[1])
		draw.circle(screen,(255, 205, 130),center,10 )

		

class player():

	def __init__(self, x,y,currentPlanet):
		
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = 0
		self.size = 10
		self.grounded = False
		self.mass = 0.01
		self.direction = 0
		self.currentPlanet = currentPlanet

		self.dangerous = []





	def move(self):
		self.x+=self.vx*ptime  
		self.y+=self.vy*ptime

		cp, d,n = self.currentPlanet.closestPoint((self.x,self.y))
		diff = self.x-cp[0],self.y-cp[1]
		angle=atan2(diff[1],diff[0])

		difftoCenter = self.x-self.currentPlanet.center[0],self.y-self.currentPlanet.center[1]
		angToCenter = atan2(difftoCenter[1],difftoCenter[0])

		if d <= self.size:
			
			#
			self.moveDir(angle,-(d-self.size))
			speed = math.sqrt(math.pow(self.vx,2) + math.pow(self.vy,2))

			self.velocityDir(angle,speed)
			self.vx*=0.5
			self.vy*=0.5
			self.grounded = True
		else:
			self.grounded = False
			
			self.velocityDir(angToCenter,-self.mass)
	
		
		self.direction = lerp(self.direction,angle,0.01)
		self.UP = self.direction
		self.LEFT = self.direction-pi/2
		self.RIGHT = self.direction+pi/2
		self.DOWN = self.direction+pi

		self.angToCenter = angToCenter

		#print(n)
		if self.currentPlanet.hitSpikes(n) and self.grounded:
			sys.exit()

	def velocityDir(self,angle,magnitude):
		self.vx+=cos(angle)*magnitude
		self.vy+=sin(angle)*magnitude
	def moveDir(self,angle,magnitude):
		self.x+=cos(angle)*magnitude*ptime
		self.y+=sin(angle)*magnitude*ptime
	def control(self,left,right,jump):
		
		if left:
			self.moveDir(self.LEFT,1.5)
		if right:
			self.moveDir(self.RIGHT,1.5)
		if jump and self.grounded:
			self.velocityDir(self.UP,3)
			self.grounded = False

	def draw(self,screen):

		x,y = rtPoint((self.x,self.y))


		draw.circle(screen,(255,0,0),(int(x),int(y)),int(self.size*cameraScale))
		ux, uy = int(cos(self.UP+cameraRotation)*15+x),int(sin(self.UP+cameraRotation)*15+y)

		draw.line(screen,(255,255,255),(x,y),(ux,uy),3)

class planet(object):
	def __init__(self, mainPts):
		self.mainPoints = genMainPts(mainPts)
		self.center = self.getCenter()
		self.subdivPts = subDivide(self.mainPoints,4)
		self.normals = self.generateNormals()
		groundLine = 15
		self.inside = self.generateOutline(groundLine)
		self.shadows = []
		for s in range(groundLine,groundLine+10,2):
			self.shadows.append(self.generateOutline(s))


		self.objects = []

		self.spikes = self.generateSpikes()
	def generateSpikes(self):
		spikes = []

		p = 0
		while p < len(self.subdivPts)-1:
			l = random.randint(5,15)

			if l > len(self.subdivPts)-p:
				l = len(self.subdivPts)-p


			spikes.append([p,p+l])

			p+=l
			p+=random.randint(20,40)

		print(spikes)





			

		return spikes



	def generateNormals(self):
		normals = []
		for n in range(len(self.subdivPts)):
			p1 = self.subdivPts[n]
			k = n+1
			if k == len(self.subdivPts):
				k = 0
			p2 = self.subdivPts[k]

			difference = p2[0]-p1[0],p2[1]-p1[1]

			angle = atan2(difference[1],difference[0])
			angle+=pi/2
			normals.append(angle)



		return normals
	def getCenter(self):
		center = [0,0]
		for o in self.mainPoints:
			center[0]+=o[0]
			center[1]+=o[1]
		center[0]/=len(self.mainPoints)
		center[1]/=len(self.mainPoints)
		ccenterOffset = center[0]-width/2,center[1]-height/2
		center[0]-=ccenterOffset[0]
		center[1]-=ccenterOffset[1]
		for p in self.mainPoints:
			p = p[0]-ccenterOffset[1],p[1]-ccenterOffset[1]
		return center
	def generateOutline(self,depth):
		insideSkipVerts = 1

		inside = []
		for p in range(0,len(self.subdivPts),insideSkipVerts):
			pt = self.subdivPts[p]
			angle = self.normals[p]+cameraRotation
			normal = pt[0]+cos(angle)*depth,pt[1]+sin(angle)*depth
			intersects = False
			for q in range(0,len(self.subdivPts)):
				if p == q: continue
				dist = math.sqrt((normal[0]-self.subdivPts[q][0])**2 + (normal[1]-self.subdivPts[q][1])**2)

				if dist <= depth:
					intersects = True
					break
			if not intersects:
				inside.append(normal)


		return inside

	def hitSpikes(self,p):
		for s in self.spikes:
			if p >= s[0] and p <=s[1]:
				return True
		return False
	def draw(self,screen):

		self.dPoints = rtPoints(self.subdivPts)
		draw.polygon(screen,(0,100,0),self.dPoints,0)
		gfxdraw.aapolygon(screen,self.dPoints,(0,150,0))

		draw.circle(screen,(255,255,255),(int(self.center[0]),int(self.center[1])),5)
		# for p in range(len(self.dPoints)):
		# 	pt = self.dPoints[p]
		# 	angle = self.normals[p]+cameraRotation
		# 	normal = pt[0]+cos(angle)*15,pt[1]+sin(angle)*15
		# 	draw.line(screen,(255,0,0),self.dPoints[p],normal,1)
		ins = rtPoints(self.inside)
		
		draw.polygon(screen,(112, 71, 71),ins,0)
		gfxdraw.aapolygon(screen,ins,(112,71,71))

		for p in self.spikes:
			t = rtPoint(p)
			draw.lines(screen,(255,0,0),False,self.dPoints[p[0]:p[1]],4)





		#for o in self.mainPoints:
			#p = int(o[0]),int(o[1])
			#pygame.draw.circle(screen,(255,0,0),p,2)
	def closestPoint(self,pos):
		dists = []
		mi = math.inf
		closestn = 0
		for n in range(len(self.subdivPts)):
			p = self.subdivPts[n]

			dist = math.sqrt(math.pow(p[0]-pos[0],2) + math.pow(p[1]-pos[1],2))
			if dist < mi:
				mi = dist
				closestPoint=p
				closestn = n
		return closestPoint,mi, closestn

def midpoint(p1,p2):

	return (p1[0]+p2[0])/2,(p1[1]+p2[1])/2

def genMainPts(numPoints,center=(300,300)):
	points = []
	mult = pi*2/numPoints
	ang = 0
	for i in range(numPoints):
		ptAngle = i*mult
		height = random.randint(50,300)
		points.append([cos(ptAngle)*height+center[0],sin(ptAngle)*height+center[1]])

	return points
def subDivide(points,iterations = 1):
	for i in range(iterations):

		midpts = []
		for k in range(len(points)):
			aIndex = k 
			bIndex = k+1
			if (bIndex == len(points)):
				bIndex = 0
			a = points[aIndex]
			b = points[bIndex]
			#print(aIndex,bIndex)

	 
			midpts.append(midpoint(a,b))
		newPoints = []
		for n in range(len(midpts)):
			aIndex = n 
			bIndex = n+1
			if (bIndex == len(midpts)):
				bIndex = 0
			newPoints.append(midpts[n])
			md = midpoint(midpts[aIndex],midpts[bIndex])

			origMod = midpoint(md,points[bIndex])
			newPoints.append(origMod)
		points = newPoints
	return points
	print('')

test = planet(25)

ball = player(0,0,test)

coin1 = coin(300,200)

while 1:
	t = time.time()
	pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	pressed = pygame.mouse.get_pressed()
	screen.fill((100,100,255))
	if pressed[0]:
		ball.x,ball.y = pos
		#ball.vx,ball.vy = 0,0

	test.draw(screen)
	ball.move()
	ball.draw(screen)
	coin1.draw(screen)
	cameraRotation = lerp(cameraRotation,-ball.angToCenter-pi/2,0.01)

	#print(cameraRotation)
	keyPress = pygame.key.get_pressed()
	#dcameraScale = sin(time.time())
	ball.control(keyPress[pygame.K_LEFT],keyPress[pygame.K_RIGHT],keyPress[pygame.K_SPACE])
	
	fps =  1 / (time.time()-t+0.0000001)

	ptime = 60/fps

	pygame.display.flip()
