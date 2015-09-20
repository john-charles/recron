# recron - A cron replacement.

recron follows crontab syntax and aims be a drop in replacement from cron.
It is only supported by the author on debian and ubuntu.

## Rationale

The `crontab` is simple and straightforward. But cron is not. Why do you
need to install postfix to use cron? Recron is a standalone daemon which
logs to /var/log/recron in a machine parsable manor. 

## Features

- Each user has a recron crontab in their home directory.
- Each crontab is logged to a separate user directory.
- Command line status command which can be used to easily check job status.

## Simple status command example output

    > recron
    recron running 2 total jobs
    412 total runs (100% healthy) /bin/ls
     10 total runs (100% healthy) DISPLAY=:0 xeyes &