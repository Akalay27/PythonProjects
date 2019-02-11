import pygame
from pygame import draw, gfxdraw
import random
from random import randint
import math
import time
from math import sin, cos, atan2
size = width,height = (600,600)

screen = pygame.display.set_mode(size)

img1 = pygame.surfarray.pixels3d(pygame.image.load("whatthe.png"))


#print(img1)
def genrandorder(total):
	order = []
	while len(order) < total:
		r = random.randint(0,total-1)
		if r not in order:
			order.append(r)
	#print(order)
	return order
def orderRainbow(particles):
	
	for p in range(1,len(particles)):
		a = particles[p]  
		b = particles[p-1]

		if (a.hue > b.hue):
			particles[p] = b
			particles[p-1] = a

	p = 0
	for y in spacingy:
		for x in spacingx:
			particles[p].changeTarget(x,y)
			p+=1

def arrangeImage(particles,image):

	for p in particles:
		px, py = randint(0,599),randint(0,599)

		while sum(image[px,py]) == 0:
			px, py = randint(0,599),randint(0,599)

		p.changeTarget(px,py)
		#p.color = image[px,py]




class particle(object):
	def __init__(self, tx,ty):
		self.tx, self.ty = tx,ty
		self.x, self.y = (random.random()*width,random.random()*height)
		self.vx, self.vy = (0,0)
		self.color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		col = pygame.Color(self.color[0],self.color[1],self.color[2],255)
		self.hue = col.hsva[0]
		self.t = 0
	def move(self):
		self.t+=1
		difference = self.tx-self.x,self.ty-self.y
		distance = math.sqrt(math.pow(self.x-self.tx,2)+math.pow(self.y-self.ty,2))
		angle = atan2(difference[1],difference[0])
		speed = distance/10000
		#print(distance)
		self.vx+= cos(angle)*speed
		self.vy+=sin(angle)*speed
		self.x+=self.vx
		self.vx*=0.99
		self.vy*=0.99
		self.x+=self.vx
		self.y+=self.vy
	




	def draw(self,screen):
		col = self.color

		#col[0]=int(col[0]+math.sin(self.t)*50)

		draw.circle(screen,self.color,[int(self.x),int(self.y)],3)

	def distFromMouse(self,pos):

		px,py = pos
		distance = math.sqrt(math.pow(self.x-px,2)+math.pow(self.y-py,2))
		return distance
	def addVel(self,vector):
		self.vx+=vector[0]
		self.vy+=vector[1]
	def changeTarget(self,tx,ty):
		self.tx,self.ty = tx,ty

particles = []
mx, my = width//2,height//2
spacingx = range(mx-100,mx+100,5)
spacingy = range(my-100,my+100,5)
for y in spacingy:
	for x in spacingx:
		particles.append(particle(x,y))

n = 0


while 1:
	timer = time.time()
	#print(genrandorder(5))
	pos = pygame.mouse.get_pos()

	pressed = pygame.mouse.get_pressed()
	if (pressed[0] and pressed[2]):
		arrangeImage(particles,img1)
	# elif (pressed[0]):
	# 	neword = genrandorder(len(particles))
	# 	i = 0
	# 	for y in spacingy:
	# 		for x in spacingx:
				
	# 			particles[neword[i]].changeTarget(x,y)

	# 			i+=1
	elif (pressed[1]):
		orderRainbow(particles)

	



	elif (pressed[2]):
		#particles[n].changeTarget(pos[0],pos[1])
		
		n+=1
		if (n > len(particles)-1):
			n = 0
		particles[n].changeTarget(pos[0],pos[1])
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	screen.fill((0,0,0))
	for p in particles:
		p.draw(screen)
		p.move()
		if (p.distFromMouse(pos) < 50):
			difference = (pos[0]-p.x,pos[1]-p.y)
			angle = atan2(difference[1],difference[0])
			p.vx-=cos(angle)*2
			p.vy-=sin(angle)*2

	print(1/(time.time()-timer))

	pygame.display.flip()
