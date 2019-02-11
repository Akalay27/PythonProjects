import pygame
import sys
import math
import time
import texMap
from math import cos, sin, pi
from pygame import draw
size = width, height = (600,600)

screen = pygame.Surface(size)
final = pygame.display.set_mode(size)

def drawCube(screen,x,y,w,h,r):
	points = []
	t = h/5
	points.append([int(cos(r)*w)+x,int(sin(r)*t)+y-h/2])
	points.append([int(cos(r)*w)+x,int(sin(r)*t)+y+h/2])

	points.append([int(cos(r+pi/2)*w)+x,int(sin(r+pi/2)*t)+y-h/2])
	points.append([int(cos(r+pi/2)*w)+x,int(sin(r+pi/2)*t)+y+h/2])

	points.append([int(cos(r+pi)*w)+x,int(sin(r+pi)*t)+y-h/2])
	points.append([int(cos(r+pi)*w)+x,int(sin(r+pi)*t)+y+h/2])

	points.append([int(cos(r+pi*1.5)*w)+x,int(sin(r+pi*1.5)*t)+y-h/2])
	points.append([int(cos(r+pi*1.5)*w)+x,int(sin(r+pi*1.5)*t)+y+h/2])
	b = 2
	col = (0,0,255)
	# for p in points:
	# 	draw.circle(screen,col,p,int(b*0.5))
	draw.polygon(screen,col,[points[0],points[1],points[3],points[2]],b*1)
	draw.polygon(screen,col,[points[4],points[5],points[3],points[2]],b*1)
	draw.polygon(screen,col,[points[4],points[5],points[7],points[6]],b*1)
	draw.polygon(screen,col,[points[0],points[1],points[7],points[6]],b*1)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	t = time.time()
	screen.fill((0,0,0))


	for y in range(0,650,50):
		for x in range(0,700,200):
			r = sin(t+(y/2)+x)*2
			drawCube(screen,x,y,100,50,r)
	

	

	


		
	# reflect = pygame.transform.flip(screen,False,True)
	# reflect = pygame.transform.smoothscale(reflect,(200,100))
	# reflect = pygame.transform.smoothscale(reflect,(600,300))
	# final.blit(screen,(0,0))
	# final.blit(reflect,(0,400))
	final.blit(screen,(0,0))


	pygame.display.flip()
