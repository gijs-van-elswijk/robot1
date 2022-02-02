
# Robot is a class with a dictionary that links to sensors/motors
# and a name that is used to subscribe to a Publisher object
# Function defined in this class can be registered to Publisher
# events. When events are send to the publisher the callbacks are 
# triggered.
class Robot:
    def __init__(self, name, modules, alive = True) -> None:
        self.name    = name
        self.modules = modules
        self.alive   = True
 
    def error(self, message = None):
        print('ERROR: {}'.format(message))

    def kill(self):
        self.alive = False
    
    def beep(self):
        if 'brick' in self.modules:
            self.modules['brick'].speaker.beep(2000, 50)
        else:
            self.error('No brick')

    def backward(self):
        if 'drivebase' in self.modules:
            self.modules['drivebase'].straight(-100)
        else:
            self.error('No drivebase')

    def turn(self):
        if 'drivebase' in self.modules:
            self.modules['drivebase'].turn(45)
        else:
            self.error('No drivebase')


class Publisher:
    def __init__(self, events) -> None:
        self.events = { event : dict() # dictionary comprehension, init dict() for every event
                    for event in events }

    def get_subscribers(self, event):
        if event in self.events:
            return self.events[event]
        else:
            print('Event {} not known to publisher'.format(event))
            return dict()
    
    def register(self, event, who, callback = None):
        self.get_subscribers(event)[who] = [ callback ]
    
    def unregister(self, event, who):
        del self.get_subscribers(event)[who]
    
    def add(self, event, who, callback):
        self.get_subscribers(event)[who].append(callback)
  
    def dispatch(self, event):
        if event is not None:
            for subscriber, callback in self.get_subscribers(event).items():
                print('Dispatching {} callbacks for subscriber: {}'.format(event, subscriber.name))
                for cb in callback:
                    cb()


class Event:
    def __init__(self, reference) -> None:
        self.occurred  = False
        self.reference = reference
     
    # detection code goes here
    def check(self) -> bool:
        self.occurred = False
        return self.occurred
 
    

# Event queue class
class Eventqueue:
    def __init__(self, events = dict()) -> None:
        self.events = events
        self.queue  = tuple()

    def occurred_events(self):
        queue = list()
        for name, ev in self.events.items():
            if ev.check():
                queue.append(name)
            self.queue = tuple(queue)
        return(self.queue)

