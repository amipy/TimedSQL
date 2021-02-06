# TimedSQL
Requires psycopg2

Example JSON query:
{"time": "22:59", "query": "INSERT INTO timexe.items(name, cost) VALUES ('Book', 34);", "amount": 100, "pause": 1000}

This means:
At 22:59, run the specified query 100 times, with an interval of 1000 milliseconds between each run.
Will attempt to run querys in parralel, but might be a few milliseconds off sometimes.
