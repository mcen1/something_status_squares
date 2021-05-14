#!/bin/env python3
# check our json during build to ensure it's actually json
import json
import sys

with open('/var/www/cgi-bin/powerdash.json') as f:
  data = json.load(f)

if str(type(data))=="<class 'dict'>":
  print("json is valid")
else:
  print("json is invalid!")
  sys.exit(1)
