from os import system, name as __UserOS__
from time import sleep
from threading import Thread

def UnixController(game,snake):
    import sys, tty, termios
    dir = {65:0,67:1,66:2,68:3}
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(sys.stdin.fileno())
    while game['running']:
        ch = ord(sys.stdin.read(1))
        if ch == 27:
            ch = ord(sys.stdin.read(2)[1:])
            snake['direction'] = dir.get(ch)
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


def Game(game,snake):
	position = snake['position']
	printable = game['screen']

	x,y = position[0]
	printable[y][x] = 'S'

	for pos in position[1:]:
		x,y = pos
		printable[y][x] = 'o'

	while game['running']:
		direction = snake['direction']
		x1,y1 = position[0]
		if direction % 2:
			x2,y2 = (x1-(direction-2),y1)
		else:
			x2,y2 = (x1,y1+(direction-1))

		x3,y3 = position[-1]

		printable[y1][x1] = 'o'
		printable[y2][x2] = 'S'
		printable[y3][x3] = ' '

		position.insert(0,(x2,y2))
		position.pop()

		clear_screen()

		for row in printable:
			print ''.join(row)

		sleep(0.04)


def main(width,height):
	game = {\
				'running':False,\
				'screen':[[' ' for i in range(width-1)] for i in range(height)],\
				'score':0,\
				'food':tuple()
			}

	x,y = (width/2,height/2)
	snake = {\
				'direction':1,\
				'position':[(x-i,y) for i in range(1,20)]\
			}


	resize(width,height)
	game['running'] = True
	controller = Thread(target=keyInput,args=(game,snake))
	controller.setDaemon(True)
	controller.start()
	Game(game,snake)

main(50,30)
