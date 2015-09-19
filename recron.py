import time
from recron.timer import MinuteTimer

class HelloTask(MinuteTimer):
    
    def __init__(self):
        MinuteTimer.__init__(self)
        
    def task(self):
        print("Hello, the time is now: ", time.asctime())
        raise Exception("Exc")
        
if __name__ == '__main__':
    ht = HelloTask()
    ht.start()