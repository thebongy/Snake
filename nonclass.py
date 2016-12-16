from os import system
from time import sleep
from msvcrt import getch
from threading import Thread

system('mode 50,30')
game_running = True
direction = 1
delay = 0.07

def clear():
	system('cls')

def controller():
	global game_running,direction,delay
	while game_running:
		key = ord(getch())
		if key == 27:
			game_running = False
		elif key == 224:
			key = ord(getch())
			if key == 72:
				direction = 0
			elif key == 80:
				direction = 1
			elif key == 77:
				direction = 2
			elif key == 75:
				direction = 3
		elif key == 102:
			delay -= 0.01
		elif key == 115:
			delay += 0.01

		

def main():
	global direction
	snake = 'S'
	snake_pos = [0,0]
	screen = [' '*49 for i in range(30)]
	size = (30,49)
	inputs = Thread(target=controller)
	inputs.start()
	def blit_snake(x2,y2):
		x1,y1 = snake_pos
		screen[x1] = screen[x1][:y1] + ' ' + screen[x1][y1+1:]
		screen[x2] = screen[x2][:y2] + snake + screen[x2][y2+1:]
		snake_pos[0],snake_pos[1] = x2,y2
	
	blit_snake(0,0)
	while game_running:
		if direction == 0:
			blit_snake(snake_pos[0]-1,snake_pos[1])
		elif direction == 1:
			blit_snake(snake_pos[0]+1,snake_pos[1])
		elif direction == 2:
			blit_snake(snake_pos[0],snake_pos[1]+1)
		else:
			blit_snake(snake_pos[0],snake_pos[1]-1)
		clear()
		if snake_pos[0] == size[0]-1:
			direction = 0
		elif snake_pos[0] == 0:
			direction = 1
		elif snake_pos[1] == size[1]-1:
			direction = 3
		elif snake_pos[1] == 0:
			direction = 2
		for i in screen:
			print i,
		sleep(delay)

main()