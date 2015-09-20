
import os, json

LOG_DIR = "/var/log/recron"
EVENTS_LOG = "events.log"

def get_job_filter(command):
    
    def job_filter(job_info):
        return job_info['command'] == command
    
    return job_filter

class EventList:
    
    def __init__(self, username):
        self.username = username
        self.event_list = []
        
    def load_events(self):
        
        events_file = os.path.join(LOG_DIR, self.username, EVENTS_LOG)
        
        with open(events_file, 'rb') as events_stream:
            
            for line in events_stream.readlines():
                line = line.decode('utf-8').strip()
                self.event_list.append(json.loads(line))
                
    def get_job_health(self, command):
        
        count_success = 0
        job_runs = list(filter(get_job_filter(command), self.event_list))
        
        for event in job_runs[-5:]:
            if event['status'] == 0:
                count_success += 1
                
        return len(job_runs), float(count_success) / len(job_runs[-5:])
    
    def get_jobs(self):
        
        job_set = set()
        
        for event in self.event_list:
            job_set.add(event['command'])
            
        return job_set
        
    