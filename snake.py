from msvcrt import getch

#Global direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


#------------------------------------------------------------
#EVENT OBJECTS

class Event():
    '''
    The Event Base class which all other events subclass from.
    '''
    def __init__(self):
        self.name = "Event"


class IterEvent(Event):
    '''
    The Event which is run on every iteration of the main program loop.
    '''
    def __init__(self):
        self.name == "New Iteration"

class MoveInputEvent(Event):
    '''
    This event is fired when the user inputs a directional key on the keyboard.
    Args:
    -direction: Stores the direction of the input in the form of the Global Direction Constants
    '''
    def __init__(self,direction):
        self.name = "Input"
        self.direction = direction


#------------------------------------------------------------
# Main Program Objects

class EventManager():
    '''
    Registers 'event listeners' and posts events to all the event listeners, via their .Notify() method.
    (An event listener must have a .Notify() method)
    '''
    def __init__(self):
        from weakref import WeakKeyDictionary # Weakref used to Build Weak-references to objects, which do not deter with garbage collection processes.
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self,listener):
        '''
        Register a listener in the Dict of listeners
        '''
        self.listeners[listener] = 1

    def UnregisterListener(self,listener):
        '''
        Remove a listener from the Dict of listeners.
        '''
        if listener in self.listeners():
            del self.listeners[listener]

    def Post(self,event):
        '''
        Notify all listeners about an ongoing event.
        '''
        for listener in self.listeners.keys():
            listener.Notify(event)

class CPUController():
    '''
    Handles the main loop of the program, by repeatdly notifying other listeners about an Iteration Event.
    '''
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.running = True

    def MainLoop(self):
        while self.running: # THis is the main loop of the program, which repeatedly runs.
            event = IterEvent()
            self.evManager.Post(event)

    def Notify(self,event):
        if isinstance(event, QuitEvent):
            self.running = False

class InputController():
    # Handles Keyboard Inputs from the user. Runs on a different thread as compared to CPUController()
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

    def MainLoop(self):
        while True:
            key = ord(getch())
            if key == 27: #Escape key pressed
                ev = QuitEvent()
            elif key == 224:
                key = ord(getch()) # Get single keypress
                if key == 72:
                    ev = MoveInputEvent(UP)
                elif key == 80:
                    ev = MoveInputEvent(DOWN)
                elif key == 77:
                    ev = MoveInputEvent(RIGHT)
                elif key == 75:
                    ev = MoveInputEvent(LEFT)
            
            self.evManager.post(ev)
    
    def Notify(self,event):
        pass
