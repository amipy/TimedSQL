import psycopg2
import json
import time

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

    time.sleep(0.01)

print("Finished")



