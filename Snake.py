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
            		game['running'] = 0
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
		elif ch == 27:
			game['running'] = 0
			clear_screen()
            	elif ch == 80 or ch == 112:
                        game['running'] = 2


def press_Enter_key():
        while True:
                x=ord(getch())
                if x==13:
                        break



def paused(game):
        clear_screen()
        print '''

The game has been paused.
(for your own convenience) :)

Click the Enter key to resume your game.

'''

        press_Enter_key()
        game['running'] = 1



def UnixResize(width,height):
    	from sys import stdout
    	stdout.write("\x1b[8;%s;%st" % (height,width))


def WindowsResize(width,height):
	system('mode %s,%s' % (width,height+2))


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
	fx,fy =randint(1,width-2),randint(1,height-2)
	game['food'] = (fx,fy)
	printable[y][x] = 'S'
	printable[fy][fx] = 'X'
	
	for pos in position[1:]:
		x,y = pos
		printable[y][x] = 'o'

	while game['running']:
		direction = snake['direction']
		x1,y1 = position[0]

		if game['running'] == 1:
                        if direction % 2:
                                x2,y2 = (x1-(direction-2),y1)
                        else:
                                x2,y2 = (x1,y1+(direction-1))

                elif game['running'] == 2:
                        paused(game)

		x3,y3 = position[-1]

                if printable[y2][x2] == 'o':
                        game['running'] = 0
                else:
                        printable[y1][x1] = 'o'
                        printable[y2][x2] = 'S'

		position.insert(0,(x2,y2))
		
		if game['food'] in position[:-1]:
			game['score'] += 10
			fx,fy = (randint(2,width-2),randint(2,height-2))
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

	for i in range(17):
                if not i%3:
                        for row in printable:
                                print ''.join(row)
                        sleep(0.2)
                else:
                        clear_screen()
                        sleep(0.05)

        clear_screen()
        print "\n Ouch! That hurts. (a lot actually) :|\n"
	username = raw_input("Enter your name (in small letters): ")
	print "Enter description of this game (optional):"
	tag = raw_input()
	if tag == '':
                tag = "<undescribed>"
	Scores.append({'Name':username,'Points':game['score'],'desc':tag})
        Scores.sort(key=lambda x:x['Points'], reverse=True)
        print 'Your score has been saved succesfully!'
        press_Enter_key()
	HomeScreen()


def main(width,height):
        screen=[[' ' for i in range(width)] for i in range(height)]
        screen[0][:]=['o' for x in range(width)]
        screen[-1][:]=['o' for x in range(width)]
        for x in screen:
                x[0],x[-1]='o','o'
        
        game = {'running':0,'screen':screen,'score':0,'food': tuple()}
	x,y = (width/2,height/2)
	snake = {'direction':1,'position':[(x-i,y) for i in range(1,3)]}

	resize(width+1,height)
	game['running'] = 1
	controller = Thread(target=keyInput,args=(game,snake))
	controller.setDaemon(True)
	controller.start()
	Game(game,snake,width,height)


def details():
        clear_screen()
        print """

Here are the details of the 'Snake' (this game) :)


1.The snake, with its head 'S', body of 'o'*n,
will move about the screen bound by snake bodies!

2.Feed it by directing it towards its food 'X'.
This will elongate the snake, but earn you points!

3.Beware! The snake must not suicide.
  Or even bite off the boundary!
  If so, the GAME IS OVER!

4.Press arrow keys to navigate in the game.
  Press 'p' to pause the game in between if needed.


That's all. Press the Enter key to return Home.

"""
        press_Enter_key()
        HomeScreen()


def about():
        clear_screen()
        print '''

This is an implementation of the original Snake
purely prepared in Python.


Created by (the Admin Panel):

The following students of class 11A, NPS Inr:
1.Rishit Bansal
2.Apurva Kulkarni

3.Koushik De
for the Computer Science Project of 2016-17.


Press the Enter key to return Home.

'''
        press_Enter_key()
        HomeScreen()

def display_scores():
        clear_screen()
        print 'HIGHSCORES:'
        for i in Scores:
                for field in data_fields:
                        print field,i[field]
                print

        print 'Press the Enter key to return Home.'
        press_Enter_key()
        HomeScreen()

def exit_game():
        data = ''
        data_scores = list(Scores)
        if len(Scores)>= 10:
                data_scores = Scores[:10]
        with open('data.txt','w') as f:
                for i in data_scores:
                        data = data+'[Score]\n'
                        for field in data_fields:
                                data = data+'['+field+']'
                                data = data + str(i[field])
                                data = data+'\n'
                        
                f.write(data)
def HomeScreen():
        resize(width+1,height)
	buttons=('New Game', 'Rules/Details', 'Scores', 'About', 'Exit')
	screen=[[' ' for i in range(width)] for i in range(height)]
	scr_row,scr_col,l=len(screen),len(screen[0]),len(buttons)
	print_lines=[x*((scr_row-7)/l)+9 for x in range(l)]

	screen[1][(scr_col-31)/2:] = "oooooooooooooS  ooooooooooooooo"
	screen[2][(scr_col-31)/2:] = "o   __  _  _   _   _  _  __   o"
	screen[3][(scr_col-31)/2:] = "o  |__' |\ |  /_\  |_/  |__   o"
	screen[4][(scr_col-31)/2:] = "o  .__| | \| /   \ | \_ |__   o"
	screen[5][(scr_col-31)/2:] = "o                             o"
	screen[6][(scr_col-31)/2:] = "ooooooooooooooooooooooooooooooo"
	
	for i in range(l):
		blen=len(buttons[i])
		screen[print_lines[i]][(scr_col-blen)/2:]=buttons[i]
		
        x,i=0,0
        while x!=13:
                blen=len(buttons[i])
		screen[print_lines[i]][(scr_col-blen)/2-4:(scr_col-blen)/2-1]="-->"
                for row in screen:
                        print ''.join(row)
                        
                x=ord(getch())
                if x==224:
                    x=ord(getch())                
                dir = {72:0,80:1,77:1,75:0}
                if x in dir:
                    x=dir[x]
                    
                screen[print_lines[i]][(scr_col-blen)/2-4:(scr_col-blen)/2-1]='   '
                if x==1:
                        i+=1
                        if i==l:
                                i-=l
                elif x==0:
                        i-=1
                        if i==-1:
                                i+=l
                                
	if i==0:
                main(width,height)
        elif i==1:
                details()
        elif i ==2:
                display_scores()
        elif i==3:
                about()
        else:
                clear_screen()
                exit_game()


width,height=50,30
data_file = 'data.txt'
Scores = []
current=None
data_fields = ['Name','desc','Points']
with open(data_file,'r') as f:
        for line in f:
                if line.find('[Score]') != -1:
                        if current != None:
                                Scores.append(current)
                        current = {'Name':'','desc':'','Points':0}
                for field in data_fields:
                        s = line.find('['+field+']')
                        if s != -1:
                                current[field] = line[len(field)+2:-1]
                                break
        if current!=None:
                Scores.append(current)

print Scores
for i in Scores:
        i['Points'] = int(i['Points'])

Scores.sort(key=lambda x:x['Points'], reverse=True)


                        
HomeScreen()                   
                        
                

