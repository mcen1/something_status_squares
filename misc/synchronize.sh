#!/bin/bash
cd /misc
python3 initdb.py
while true; do
python3 statuscheck.py > /misc/statuscheck.log; sleep 60;
done
