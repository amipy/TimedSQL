import psycopg2
import json
import time
import math
import datetime

from Command import Command

with open("timexe_config.json") as conf_file:
    config=json.load(conf_file)
#print(config)
dbase=psycopg2.connect(host=config["host"], database=config["db"], user=config["user"], password=config["pass"])

cursor=dbase.cursor()
#cursor.execute("SELECT * FROM timexe.testington;")
#print(cursor.fetchall())


commands = []
for cmnd in config['commands']:
    commands.append(Command(dbase, cmnd['query'], cmnd['time'], cmnd['amount'], cmnd['pause']))

intervals=[]
for i in commands:
    intervals.append(i._pause)

min_interval=intervals[0]
if len(intervals)>1:
    min_interval=math.gcd(*intervals)

minty=commands[0]._startTime
min_time=commands[0]._startTimeDT
for i in commands:
    if i._startTimeDT<=min_time:
        min_time=i._startTimeDT
        minty=i._startTime

#print(min_interval)
running = True
dtnow = datetime.datetime.now()
while dtnow.replace(year=dtnow.year, month=dtnow.month, day=dtnow.day)<min_time:
    dtnow = datetime.datetime.now()
    print(min_time-dtnow.replace(year=dtnow.year, month=dtnow.month, day=dtnow.day, microsecond=0))
    time.sleep(1)
print("Executing.")
while running:
    finish = True
    for c in commands:
        c.execute()
        if not c.isDone:
            finish = False
    if finish:
        running = False

    time.sleep(min_interval/1000)

print("Finished")
