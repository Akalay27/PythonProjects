import pygame
from pygame import surfarray, draw
from random import randint

size = width,height = (1050,600)

screen = pygame.display.set_mode(size)
def Wheel(wheelPos): #transfered cpp function from adafruit.com's led functions into python 
    
    wheelPos = wheelPos
    if (wheelPos < 85):
        
        return 255-wheelPos*3,0,wheelPos
    elif (wheelPos < 170):
        wheelPos -= 85
        return 0,wheelPos*3,255-wheelPos*3
    else:
        wheelPos -= 170
        return wheelPos*3,255-wheelPos*3,0

arr = surfarray.pixels3d(screen)
for yp in range(0,height):
	for xp in range(0,width):
		x0 = xp*(3.5/width)-2.5
		y0 = yp*(2/height)-1

		x = 0.0
		y = 0.0
		iteration = 0
		maxIteration = 50
		while x*x + y*y <=2*2 and iteration < maxIteration:
			xtemp = x*x-y*y + x0
			y = 2*x*y + y0
			x = xtemp
			iteration+=1
		col = int((iteration/maxIteration)*255)


		arr[xp,yp] = Wheel(col)
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	pygame.display.flip()