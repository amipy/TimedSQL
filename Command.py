import datetime
import time

import psycopg2


class Command:
    _started = False
    _amount = 0

    def __init__(self, dbase, query, startTime, amount, pause):
        self._query = query
        self._startTime = startTime
        self._amountLimit = amount
        self._pause = pause
        self._dbase = dbase
        self._cursor = dbase.cursor()

        dt = datetime.datetime.strptime(self._startTime, "%H:%M")
        dtnow = datetime.datetime.now()
        self._startTimeDT = dt.replace(year=dtnow.year, month=dtnow.month, day=dtnow.day)


    def executeOnce(self):
        self._cursor.execute(self._query)
        try:
            print(self._cursor.fetchall())
        except:
            pass
        self._dbase.commit()
        self._amount += 1

    def execute(self):
        if not self._started:
            if datetime.datetime.now() >= self._startTimeDT:
                #print(f"command {self._query} has started")
                self._started = True
                self.executeOnce()
        else:
            if not self.isDone and datetime.datetime.now() >= self._startTimeDT + datetime.timedelta(milliseconds=self._amount*self._pause):
                self.executeOnce()
                print(f"command {self._query} executed {self._amount} times")
                pass

    @property
    def isDone(self):
        return self._amount >= self._amountLimit

    def __str__(self):
        return (self._query)