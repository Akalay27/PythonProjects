import pygame
import sys
from pygame import draw, surfarray
import numpy
import random
pygame.init()
size = width,height = (1200,1200)
actualRes = (100,100)
screen = pygame.display.set_mode(size)
scr = pygame.Surface(actualRes)
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
class ball(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.r = random.random()+0.3
		self.vel = [random.random()*3-1.5,random.random()*3-1.5]

	def show(self,scr):
		#draw.circle(scr,(255,255,255),(int(self.x),int(self.y)),1)
		

		if (self.x > actualRes[0] or self.x < 0):
			self.vel[0]*=-1

		if (self.y > actualRes[1] or self.y < 0):
			self.vel[1]*=-1
		self.x+=self.vel[0]
		self.y+=self.vel[1]
		
def dist(p0, p1):
    return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2


balls = []

for b in range(5):
	balls.append(ball(random.randint(0,actualRes[0]),random.randint(0,actualRes[1])))
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	scr.fill((0,0,0))

	arr = surfarray.pixels3d(scr)

	for y in range(actualRes[1]):
		for x in range(actualRes[0]):
			s = 0
			for b in balls:
				d = (1*b.r)/(dist((b.x,b.y),(x,y))+0.01)
				s+=d*100
				#b.show(scr)
	
			arr[x,y] = (constrain(s*255,0,255),0,0)
	for b in balls:
		b.show(scr)
	screen.blit(pygame.transform.smoothscale(scr,size),(0,0))
	print("test")
	pygame.display.flip()







