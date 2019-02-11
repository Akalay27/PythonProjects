import curses
from curses import wrapper
import time
import cv2


def main (stdscr):
	cap = cv2.VideoCapture(0)
	f = open("askiigradient.txt","r")
	index = f.read().split("\n")
	index = [" ",".","o","O","0","@"]
	f.close()
	colorRes = len(index)
	stdscr.clear()
	
	stdscr.nodelay(True)
	height,width = stdscr.getmaxyx()
	# width = 30
	# height = 30
	while 1:
		_, frame = cap.read()
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		small = cv2.resize(frame,(width,height))
		stdscr.move(0,0)
		for y in range(height):
			for x in range(width):

				#if stdscr.inch(y,x-1) != index[int((small[y][x]/255)*colorRes)]:
				stdscr.addstr(index[int((small[y][x]/255)*colorRes)])
				#stdscr.move(y,x)
			stdscr.move(y,0)	
		stdscr.refresh()
				
			
		if (stdscr.getch() == ord('e')):
			break

wrapper(main)