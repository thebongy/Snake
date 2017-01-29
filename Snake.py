from os import system, name as __UserOS__
from time import sleep,clock
from threading import Thread
from random import randint

SPEED = 0.08
def UnixController(game,snake):
    import sys, tty, termios
    current = snake['direction']
    dir = {65:0,67:1,66:2,68:3}
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(sys.stdin.fileno())
    while game['running']:
        ch = ord(sys.stdin.read(1))
        if ch == 27:
            ch = ord(sys.stdin.read(2)[1:])
            code = dir.get(ch)
            if code != current^2:
            	snake['direction'] = code
            	current = code
        elif ch == 112:
            game['running'] = False
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def WindowsController(game,snake):
	from msvcrt import getch
	current = snake['direction']
	dir = {72:0,80:2,77:1,75:3}
	while game['running']:
		ch = ord(getch())
		if ch == 224:
			ch = ord(getch())
			code = dir.get(ch)
			if code != current^2:
				snake['direction'] = code
				current = code
		elif ch == 27 or ch == 112:
			game['running'] = False
			clear_screen()
            #game['state'] = 2 #Pause game functionality to be implemented


def UnixResize(width,height):
    from sys import stdout
    stdout.write("\x1b[8;%s;%st" % (height,width))


def WindowsResize(width,height):
	system('mode %s,%s' % (width,height))

if __UserOS__ == 'nt':
	keyInput = WindowsController
	clear_screen = lambda:system('cls')
	resize = WindowsResize
else:
	keyInput = UnixController
	clear_screen = lambda:system('clear')
	resize = UnixResize


def Game(game,snake,width,height):
	position = snake['position']
	printable = game['screen']

	x,y = position[0]
	fx,fy =randint(2,width-2),randint(2,height-2)
	game['food'] = (fx,fy)
	printable[y][x] = 'S'
	printable[fy][fx] = 'X'

	for pos in position[1:]:
		x,y = pos
		printable[y][x] = 'o'

	while game['running']:
		x=clock()
		direction = snake['direction']
		x1,y1 = position[0]
		if direction % 2:
			x2,y2 = (x1-(direction-2),y1)
		else:
			x2,y2 = (x1,y1+(direction-1))
		
		if x2 == -1 or y2 == -1 or x2 == width or y2 == height or (x2,y2) in position:
			game['running'] = False
			break
		x3,y3 = position[-1]

		printable[y1][x1] = 'o'
		printable[y2][x2] = 'S'

		position.insert(0,(x2,y2))

		if game['food'] in position[:-1]:
			game['score'] += 10
			fx,fy = (randint(2,width-2),randint(2,height-2))
			game['food'] = (fx,fy)
			printable[fy][fx] = 'X'
		else:
			printable[y3][x3] = ' '
			position.pop()
		
		x = x-clock()
		if x < SPEED:
			sleep(SPEED-x)
		
		clear_screen()

		for row in printable:
			print ''.join(row)

		print 'Score:',game['score']

def main(width,height):
	game = {
				'running':False,\
				'screen':[[' ' for i in range(width)] for i in range(height)],\
				'score':0,\
				'food': tuple()
			}

	x,y = (width/2,height/2)
	snake = {\
				'direction':1,\
				'position':[(x-i,y) for i in range(1,3)]\
			}


	resize(width,height)
	game['running'] = True
	controller = Thread(target=keyInput,args=(game,snake))
	controller.start()
	Game(game,snake,width,height)



main(50,30)
