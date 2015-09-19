# recron - A Simple yet powerful cron replacement.

recron follows crontab syntax and should be a drop in replacement on any
linux or unix system. But it is only supported by the author on debian/ubuntu.

It aims to be simple, starting from *what do you need in a scheduler on a laptop*
Meaning that things like email support are down on the road map as optional extras
and early versions will focus strictly on things like simple file logging nothing
more complicated.

But it's design is module with the goal of having a plugin api to one day support
email notifications, or even a we portal like jenkins.

Road Map of Goals:
    
    1. Be able to parse crontab formatted files
    2. Run scripts when they are scheduled
    3. Log the results to simple flat files in /var/log/recron
    4. Multi user support
    5. Run as a Daemon
    