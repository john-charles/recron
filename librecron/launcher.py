import os, pwd, json, uuid, datetime
import logging

from crontab import CronTab
from .timer import MinuteTimer
from subprocess import Popen, STDOUT

class Job:
    
    def __init__(self, user_info, command, now, config):

        self.now = now
        self.config = config
        self.command = command
        self.user_info = user_info
        self.events_log = "events.log"
        self.user_logdir = os.path.join("/var/log/recron", user_info.pw_name)
        self.job_logfile = "%s-%s" % (now.strftime("%Y-%m-%d-%H-%M"), str(uuid.uuid4()))
        
    def run(self):
        
        if not os.path.exists(self.user_logdir):
            os.makedirs(self.user_logdir)
        
        job_args = {
            'command': self.command,
            'user_id': self.user_info.pw_uid,
            'logfile': os.path.join(self.user_logdir, self.job_logfile)
        }
        
        job_process = Popen(("/home/john-charles/Projects/recron/recron-launch", json.dumps(job_args)))
        job_args['status'] = job_process.wait()
        
        with open(os.path.join(self.user_logdir, self.events_log), 'ab') as log:
            log.write(json.dumps(job_args).encode('utf-8'))
            log.write(b'\n')
            log.flush()


class Launcher(MinuteTimer):
    
    def __init__(self, config):
        MinuteTimer.__init__(self)
        self.config = config
        
    def time_matches(self, job, now):
        return job.strftime("%Y-%m-%d-%H-%M") == now.strftime("%Y-%m-%d-%H-%M")
        
    def run_job(self, user_info, job_info, now):
        
        schedule = job_info.schedule()
        
        # cron iter needs to go forward then back to get the.
        # current cronjob...
        schedule.get_next()
        schedule.get_prev()
        
        if self.time_matches(schedule.get_current(), now):
            job = Job(user_info, job_info.command, now, self.config)
            job.run()
        
        
    def run_usercrontab(self, username, now):
        
        logging.debug("running jobs for: " + username)
        
        user_info = pwd.getpwnam(username)
        
        user_crontab = os.path.join(user_info.pw_dir, ".recron/crontab")
        
        if not os.path.exists(user_crontab):
            logging.warning("crontab for: " + username + " not found!")
        else:
            crontab = CronTab(tabfile=user_crontab)
            logging.debug("loaded crontab for: " + username)
            
            for job in crontab.crons:
                self.run_job(user_info, job, now)
            

    def task(self):
        
        logging.info("launching jobs")
        
        now = datetime.datetime.now()
        
        for username in self.config.active_user_list:
            self.run_usercrontab(username, now)