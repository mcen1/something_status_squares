#!/bin/env python3
import json
import os
import ssl
import urllib.request
import base64
import sqlite3
import time
# How many entries to pad out to if different sites have different numbers. Should be the same number as initdb.py's.
MAXDB=16
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# this code assumes you have 1 set of credentials for your web request. If not, you'll probably need to modify this code a bit to suit your needs
username="someuser"
password="somepassword"
from datetime import datetime

with open('/var/www/cgi-bin/powerdash.json') as f:
  data = json.load(f)

def checkPing(toping):
  response = os.system("ping -c 1 -w 5 " + str(toping) +" > /dev/null 2>&1")
  if response == 0:
    return "ok"
  else:
    response = os.system("ping -c 1 -w 5 " + str(toping) +" > /dev/null 2>&1")
    if response == 0:
      return "ok"
    else:
      return "error"

def getUrl(targeturl,searchstring):
  targeturl=targeturl.replace(" ","%20")
  req = urllib.request.Request(targeturl)
  credentials = ('%s:%s' % (username, password))
  encoded_credentials = base64.b64encode(credentials.encode('ascii'))
  req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
  myout=""
  try:
    response=urllib.request.urlopen(req, context=ctx)
    myout=response.read().decode()
  except Exception as e:
    print("Exception in getUrl function call:" +str(e))
  if searchstring.lower() in myout.lower():
    return "ok"
  return "error"
conn = sqlite3.connect('/var/www/cgi-bin/database.db')
for site in data:
  sitename=site
  siteurl="none"
  checkresults=[]
  queryresults=[]
  print(sitename)
  try:
    siteurl=data[site]["linkurl"]
  except:
    pass
  for item in data[site]['siteitems']:
    itemheader=item
    print("Checking "+sitename+"'s "+str(item['name']))
    mystatus="error"
    if item['method']=='http':
      mystatus=getUrl(item['url'],item['string'])
    if item['method']=='ping':
      mystatus=checkPing(item['url'])
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    checkresults.append(str(item['name'])+":"+mystatus+":"+str(current_time))
    print(str(item['name'])+":"+mystatus+":"+str(current_time))
  # pad out our check results to have MAXDB entries
  checkresults += ['none'] * (MAXDB - len(checkresults))
  allresults=', '.join(f'"{w}"' for w in checkresults)
  myquery="delete from powerstatus where sitename='"+sitename+"'" 
  conn.execute(myquery)
  myquery="insert into powerstatus values(\""+sitename+"\",\""+siteurl+"\","+allresults+")"
  conn.execute(myquery)
  conn.commit()

