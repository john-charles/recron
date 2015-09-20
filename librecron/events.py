
import os, json

LOG_DIR = "/var/log/recron"
EVENTS_LOG = "events.log"

class EventList:
    
    def __init__(self, username):
        self.username = username
        self.event_list = []
        
    def load_events(self):
        
        events_file = os.path.join(LOG_DIR, self.username, EVENTS_LOG)
        
        with open(events_file, 'rb') as events_stream:
            
            for line in events_stream.readlines():
                line = line.decode('utf-8').strip()
                self.events_list.append(json.loads(line))
                
    def get_job_health(self):
        
        count_success = 0
        last_five = self.events_list[-5:]
        
        for event in last_five:
            if event['status'] == 0:
                count_success += 1
                
        return float(count_success) / len(last_five)
        
    