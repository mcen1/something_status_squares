#!/bin/env python3
# initialize our sqlite3 db with MAXDB fields per row
import sqlite3
import json
import os
MAXDB=16
try:
  os.remove("/var/www/cgi-bin/database.db")
except:
  pass
with open('/var/www/cgi-bin/powerdash.json') as f:
  data = json.load(f)


conn = sqlite3.connect('/var/www/cgi-bin/database.db')
print("Opened database successfully")
mytables=[]
for x in range(0, MAXDB):
  mytables.append("item"+str(x)+" TEXT")
try:
  allres= ",".join(mytables)
  conn.execute('CREATE TABLE powerstatus (sitename TEXT UNIQUE, url TEXT, '+allres+')')
  for sitename in data:
    conn.execute("insert into powerstatus(sitename) Values ('%s');" % (sitename))
except Exception as e:
  print(e)
  pass


print("Table created successfully")
conn.close()
