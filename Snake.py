from os import system, name as __UserOS__
from time import sleep
from threading import Thread
from random import randint


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
	from msvcrt import getch
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
	fx,fy =randint(1,width-1),randint(1,height-1)
	game['food'] = (fx,fy)
	printable[y][x] = 'S'
	printable[fy][fx] = 'X'
	
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

		position.insert(0,(x2,y2))
		
		if game['food'] in position[:-1]:
			game['score'] += 10
			fx,fy = (randint(2,width-1),randint(2,height-1))
			game['food'] = (fx,fy)
			print fy,fx
			print len(printable)
			printable[fy][fx] = 'X'
		else:
			printable[y3][x3] = ' '
			position.pop()
			
		clear_screen()

		for row in printable:
			print ''.join(row)
		
		print 'Score:',game['score'],game['food']
		sleep(0.1)


def main(width,height):
        screen=[[' ' for i in range(width-1)] for i in range(height)]
        game = {'running':False,'screen':screen,'score':0,'food': tuple()}

	x,y = (width/2,height/2)
	snake = {'direction':1,'position':[(x-i,y) for i in range(1,3)]}

	game['running'] = True
	controller = Thread(target=keyInput,args=(game,snake))
	controller.setDaemon(True)
	controller.start()
	Game(game,snake,width,height)


def HomeScreen(screen):
        resize(width,height)
	buttons=('New Game','Scores','Exit')
	scr_row,scr_col,l=len(screen),len(screen[0]),len(buttons)
	print_lines=[x*((scr_row-10)/(l+1))+5 for x in range(l)]
	
	for i in range(l):
		blen=len(buttons[i])
		screen[print_lines[i]][(scr_col-blen)/2:(scr_col+blen)/2]=buttons[i]
		
        x,i=0,0
        while x!=13:
                blen=len(buttons[i])
		screen[print_lines[i]][(scr_col-blen-1)/2-1]=chr(62)
                for row in screen:
                        print ''.join(row)
                        
                x=ord(getch())
                if x==224:
                    x=ord(getch())                
                dir = {72:0,80:1,77:1,75:0}
                if x in dir:
                    x=dir[x]
                    
                screen[print_lines[i]][(scr_col-blen-1)/2-1]=' '
                if x==1 and i!=l-1:
                        i+=1
                elif x==0 and i!=0:
                        i-=1
                        
	if i==0:
                main(width,height)
        else:
                exit()


width,height=50,30
screen=[[' ' for i in range(width-1)] for i in range(height)]
HomeScreen(screen)
