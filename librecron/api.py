'''
This will eventually be refactored out somewhere ehse.
'''
import io
import os
import json
from .config import CONFIG
from crontab import CronTab


class JobExecution:
    
    start = None
    duration = None
    
    def __init__(self, event):
        self.event = event
    
    @property
    def status(self):
        return "SUCCESS" if self.event['status'] == 0 else "FAILURE"
    
    @property
    def status_code(self):
        return self.event['status']
    
    def get_output(self):
        try:
            return open(self.event['logfile'], 'rb')
        except FileNotFoundError:
            return io.StringIO()

class Job:
    
    name = None
    command = None
    history = None
    
    def __init__(self, cronentry, history_events):
        self.cronentry = cronentry
        self.history = list(map(lambda e: JobExecution(e), history_events))
    
    @property
    def status(self):
        return list(self.history)[-1].status
    
    @property
    def health(self):
        
        count_success = 0
        health_history = self.history[-5:]
        
        for event in health_history:
            if event.status == 'SUCCESS':
                count_success += 1
                
        return len(self.history), float(count_success) / (len(health_history) or 1)
    
    @property
    def schedule(self):
        return self.cronentry.schedule()

class Api:
    
    events_list = None
    
    def __init__(self):
        self.events_list = []
    
    def load_events(self):
        
        events_list = []
        events_file = os.path.join(CONFIG.LOG_DIR, CONFIG.username, CONFIG.EVENTS_LOG)
        
        try:
        
            with open(events_file, 'rb') as events_stream:
                
                for line in events_stream.readlines():
                    line = line.decode('utf-8').strip()
                    events_list.append(json.loads(line))
                    
            self.events_list = events_list
            
        except FileNotFoundError:
            pass
        
        return self.events_list
            
    def load_crontab(self):
        
        tabs = []
        
        try:
        
            with open(CONFIG.user_crontab, 'rb') as crontab_stream:
                
                for line in crontab_stream.readlines():
                    if not line.strip().startswith(b'#'):
                        tabs.append(line.strip().decode("utf-8"))
                        
        except FileNotFoundError:
            pass
                    
        return tabs
    
    def map_job(self, job_line):
        
        crontab = CronTab(tab=job_line)
        cronentry = crontab.crons[0]
        
        history_events = filter(lambda e: e['command'] == cronentry.command,
                                self.load_events())
        
        job = Job(cronentry, history_events)
        job.command = cronentry.command
        
        return job
    
    def get_jobs(self):
        
        tabs = self.load_crontab()
        jobs = map(self.map_job, tabs)
        return sorted(jobs, key=lambda job: job.command)
    
    def create_job(self, name):
        return None
    
    def delete_job(self, name):
        pass
    
    def connect(self, event, name_or_cb, cb=None):
        pass

