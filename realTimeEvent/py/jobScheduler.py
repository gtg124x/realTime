#!/usr/bin/env python

from apscheduler.schedulers.blocking import BlockingScheduler

import subprocess

sched = BlockingScheduler()


def timed_job():
    subprocess.call("./EventRetriever.py", shell=True)

sched.add_job(timed_job, 'interval', hours=1)
sched.start()