#Adam Kalayjian
#2018
#Sorting vis thing

# # # PROGRAM VARIABLES # # #

size = width,height = (1920,1080)
numParticles = 75;
amountOfScreen = 3;

# # # # # # # # # # # # # # # 

import pygame
import random
from pygame import draw
from pygame.locals import *
import sys
import time
import math
from math import atan2, cos, sin

screen = pygame.display.set_mode(size,pygame.HWSURFACE)
values = []

particles = []
useParticles = True
accessCount = 0
for i in range(0,numParticles):
	values.append(i)
currentTime = 0
timeScalar = 1
modified = []
totalSwaps = 0
wait = True

groupLeft, groupRight = 0,0;
#values = [1,2,3,4,5,6,7,8]

#1200 elements merge - 363665
#1200 elements bubble - 347585
#1200 elements insertion - 359210
#1200 elements bubble merge - 360648

		
class particle(object):
	def __init__(self, tx,ty,col,val):
		self.tx, self.ty = tx,ty
		self.x, self.y = tx,ty
		self.vx, self.vy = (0,0)
		self.color = col
		self.hue = pygame.Color(self.color[0],self.color[1],self.color[2],255).hsva[0]
		self.value = val
	def move(self,dt):
		
		difference = self.tx-self.x,self.ty-self.y
		distance = math.sqrt((self.x-self.tx)**2+(self.y-self.ty)**2)
		angle = atan2(difference[1],difference[0])
		speed = distance/100
		#print(distance)
		self.vx+= cos(angle)*speed
		self.vy+=sin(angle)*speed
		self.x+=self.vx*dt
		self.y+=self.vy*dt
		self.vx*=0.90
		self.vy*=0.90
	def draw(self,screen):
		draw.circle(screen,self.color,[int(self.x),int(self.y)],int(width/len(particles)/2))
	def changeTarget(self,tx,ty):
		self.tx,self.ty = tx,ty

def addParticles(values):
	particles = []

	drawHeight = height-100
	ratioH = drawHeight/max(values)
	widthOfRect = width/len(values)
	colorRatio = 360/max(values)

	for v in range(len(values)):
		col = pygame.Color(0,0,0)
		col.hsva = (colorRatio*values[v],100,100)
		particles.append(particle(widthOfRect*v,height-values[v]*ratioH,col,values[v]))
	return particles

def drawParticles(screen):
	global currentTime
	screen.fill((0,0,0))
	drawHeight = height-100
	ratioH = drawHeight/max(values)
	widthOfRect = width/len(values)
	colorRatio = 360/max(values)
	deltaTime = 0.2+(time.time()-currentTime)/timeScalar

	draw.rect(screen,(30,30,30),(groupLeft*widthOfRect-(width/len(particles)/2),0,(groupRight-groupLeft)*widthOfRect+(width/len(particles)),height))
	for p in particles:
		p.move(deltaTime);
		p.draw(screen)
		if p.value in values:
			index = values.index(p.value)
			p.changeTarget(widthOfRect*index,height/2+height/amountOfScreen/2-p.value*height/amountOfScreen/len(particles))#height-p.value*ratioH)
	currentTime = time.time();
	pygame.display.flip()

def scrambleValues(values,iterations):

	iterations*=len(values)
	for i in range(iterations):
		rand1 = random.randint(0,len(values)-1)
		rand2 = random.randint(0,len(values)-1)
		if rand1 != rand2:
			swap(values,rand1,rand2,addM=False)

	accessCount=0

def addModified(*nums):
	global modified
	global accessCount
	modified.extend(nums)
	accessCount+=len(nums)
	#drawValues(screen,values)
	return

def swap(values,a,b,addM=True):
	swap = values[a]
	values[a] = values[b]
	values[b] = swap
	if addM:
		addModified(a,b)
	return

def selection(values, draw=True,start=0,end=-1):
	if end == -1:
		end = len(values)
	for v in range(start,end):
		pauseUntilSpace()

		m = values[v];
		vm = v;
		for c in range(v+1,end):
			print(c)
			if (values[c] < m):
				m = values[c]
				vm = c
		swap(values, v, vm)

		if draw:
			drawValues(screen,values)


def bubble(values,draw=True,start=1,end=-1):
	if end == -1:
		end = len(values)
	for v in range(start,end):
		for v in range(start,end):
			if values[v-1] > values[v]:
		
				swap(values,v-1,v)
		if draw:
			drawValues(screen,values)

def insertion(values,draw=True,start=0,end=-1,cur=-1):
	
	if cur < 0:
		i = start+1
	else:
		i=cur
	if end == -1:
		end = len(values)
	
	while i < end: 
		j = i
		#print(i,j)
		pauseUntilSpace()
		while j > start and values[j] < values[j-1]:
			swap(values,j,j-1,addM=True)
			j-=1
			addModified(j,j-1)
		i+=1

		
		if draw:
			drawValues(screen,values)
			
def bottomUpMerge(values,draw=True,start=0,mid=0,end=0):
	global groupLeft, groupRight
	i = 0
	j = 0
	
	#print((start,mid,end),values[start:end+1])
	left = values[start:mid+1]
	right = values[mid+1:end+1]

	groupLeft, groupRight = start,end
	emptySide = 0
	pauseUntilSpace();
	for k in range(start,end+1): #all of this extra stuff is to make sure the program doesnt crash when dealing with slices of 2 and for comparing array indecies that dont exist.
		addLeft,addRight = False,False
		if emptySide == 2:
			addLeft = True
		elif emptySide == 1:
			addRight = True
		elif left[i] < right[j] or j > end:
			addLeft = True
		else:
			addRight = True
		if addLeft:
			values[k] = left[i]
			i+=1
			#print("Used left")
			addModified(k,i+start)
			if i >= len(left):
				emptySide = 1
		else:
			values[k] = right[j]
			j+=1
			#print("Used right")
			addModified(k,j+mid)
			if j >= len(right):
				emptySide = 2
		#print(values[k])
		if draw:
			
			drawValues(screen,values)
	
def merge(values,start=0,end=-1,recur=0):
	global groupLeft, groupRight
	if end < 0:
		end = len(values)-1
	mid = int((end-start)/2+start)
	#print(start,mid,end)
	groupLeft = start
	groupRight = end
	if end-start > 1:
		
		merge(values,start=start,end=mid,recur=recur+1)
		merge(values,start=mid+1,end=end,recur=recur+1)
	#insertion(values,draw=False,start=start,end=end,cur=mid)
	#bubble(values,draw=False,start=start,end=end)
	if start != end:

		bottomUpMerge(values,draw=True,start=start,mid=mid,end=end)
	#print(values)
	#drawValues(screen,values)
	
	pass

def pauseUntilSpace():
	global wait
	while 1:

		if useParticles:
			drawParticles(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key == K_RETURN:
				return
			if event.type == KEYDOWN and event.key == K_RSHIFT: 
				wait = not wait
			
		if not wait:
			return
def drawValues(screen,values):
	global useParticles
	global modified
	screen.fill((0,0,0))
	#print(width,height,len(values))
	drawHeight = height-100
	ratioH = drawHeight/max(values)
	widthOfRect = width/len(values)
	colorRatio = 360/max(values)
	if not useParticles:
		for v in range(len(values)):
			
			if v not in modified:
				col = pygame.Color(0,0,0)
				col.hsva = (colorRatio*values[v],100,100)
				#col = pygame.Color(255,0,0)
			else:
				col = (255,255,255)
			draw.rect(screen,col,(widthOfRect*v,height,widthOfRect,-(values[v]*ratioH)))

	else:
		drawParticles(screen)
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	pygame.display.flip()
	modified = []
	# print(accessCount)
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_p]:
		useParticles = not useParticles	



scrambleValues(values,25)
particles = addParticles(values)
while 1:
	groupLeft, groupRight = -5, -5;
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == KEYDOWN and event.key == K_RSHIFT: 
			wait = not wait
		if event.type == KEYDOWN and event.key == K_p:
			useParticles = not useParticles


	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_m]:
		merge(values)
	if pressed[pygame.K_b]:
		bubble(values)
	if pressed[pygame.K_i]:
		insertion(values)
	if pressed[pygame.K_x]:
		scrambleValues(values,25)
	if pressed[pygame.K_s]:
		selection(values)

	drawValues(screen,values)
#bubble 174750
#insertion 173146
#merge 11152

#with 1200 elements

#merge 24704
#bubble 700908
#insertion 716412

#merge is so much faster!!!!!
