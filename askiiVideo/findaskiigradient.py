from PIL import Image, ImageGrab
from ctypes import windll, Structure, c_long,byref
import time
import sys
# class POINT(Structure):
# 	_fields_ = [("x",c_long),("y",c_long)]
# def queryMousePosition():
# 	pt = POINT()
# 	windll.user32.GetCursorPos(byref(pt))
# 	return {"x":pt.x,"y":pt.y}

# print("\n\n\n\n\nPut Cursor here\n     *")
# time.sleep(2)
# pos = queryMousePosition()
# bbox = (pos["x"]-20,pos["y"]-20,pos["x"]+20,pos["y"]+20)
characters = []
index = {}
for c in range(32,127):
	characters.append(chr(c))

for c in characters:
	for y in range(0,50):
		for x in range(0,50):
			sys.stdout.write(c)
		print("")

	im = ImageGrab.grab(bbox=(0,800,400,1000))
	#im.show()
	pixels = list(im.getdata())
	
	brightnessValue = 0
	for p in pixels:
		if (sum(p) > 10):
			brightnessValue+=1
	index[brightnessValue] = c
	time.sleep(0.01)
print(index)
brightnessIndex = sorted(index)
chrs = []
for c in brightnessIndex:
	chrs.append(index[c])
print(chrs)
print(brightnessIndex)
#[3110, 14720, 32460]

for c in chrs:
	for y in range(0,50):
		for x in range(0,50):
			sys.stdout.write(c)
		print("")
	time.sleep(0.1)

f = open("askiigradient2.txt","w")

li = ""
for c in chrs:
	li+=c
	li+="\n"
f.write(li)
f.close()