# recron - A Simple yet powerful cron replacement.

recron follows crontab syntax and aims be a drop in replacement from cron.
It is only supported by the author on debian and ubuntu.

It aims to be simple, starting from *what do you need in a scheduler on a laptop.*
And then implementing more advance features later after the core is solid.

Road Map of Goals:
    
    1. Be able to parse crontab formatted files
    2. Run scripts when they are scheduled
    3. Log the results to simple flat files in /var/log/recron
    4. Multi user support
    5. Run as a Daemon
    