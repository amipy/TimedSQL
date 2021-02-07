import psycopg2
import json
import time
import math

from Command import Command

with open("timexe_config.json") as conf_file:
    config=json.load(conf_file)
print(config)
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

print(min_interval)
running = True
print("The program is running...")
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



