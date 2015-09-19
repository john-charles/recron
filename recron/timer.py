import time
from threading import Event, Thread

def get_current_minute():
    return time.strftime("%M")

class MinuteTrigger(Thread):
    """
    Triggers an event as close as possible to the first
    second of a minute.
    
    Resolution is one second + processor time and system
    factors...
    """
    def __init__(self, event):
        Thread.__init__(self)        
        self.event = event
        self.running = True
        self.current_minute = get_current_minute()
        
    def stop(self):
        self.running = False
        
    def run(self):
        
        while self.running:
            
            current_minute = get_current_minute()
            if self.current_minute != current_minute:
                self.current_minute = current_minute
                self.event.set()
                
            time.sleep(1)
            

class MinuteTimer(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        
        self.__event = Event()
        self.running = True
        self.minute_trigger = MinuteTrigger(self.__event)
        
    def stop(self):
        self.minute_trigger.stop()
        self.running = False
        
    def run(self):
        
        self.minute_trigger.start()
        
        while self.running:
            try:
                self.task()
            except Exception as e:
                print(e)
                
            self.__event.clear()
            self.__event.wait()
        
        
    def task(self):
        raise Exception("Please override this")
        
        
        
        