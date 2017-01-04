from os import system, name as __UserOS__
from time import sleep
from threading import Thread

def UnixController(game,snake):
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(sys.stdin.fileno())
    while game['running']:
        ch = ord(sys.stdin.read(1))
        if ch == 27:
            ch = ord(sys.stdin.read(2))[1:]
            if 64 < ch < 69:
                snake['direction'] = ch-65
        elif ch == 112:
            game['state'] = 2
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def WindowsController(game,snake):
    from msvcrt import getch
    while game['running']:
        ch = ord(getch())
        if ch == 224:
            ch = ord(getch())
            if ch == 72:
                snake['direction'] = 0
            elif ch == 80:
                snake['direction'] = 1
            elif ch == 77:
                snake['direction'] = 2
            elif ch == 75:
                snake['direction'] = 3
        elif ch == 27 or ch == 112:
            game['state'] = 2


if __UserOS__ == 'nts':
    keyInput = WindowsController
    clear_screen = lambda:system('cls')
else:
    keyInput = UnixController
    clear_screen = lambda:system('clear')
