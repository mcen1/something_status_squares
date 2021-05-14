#!/bin/bash

nohup bash /misc/synchronize.sh &

echo "Starting up httpd in foreground..."
httpd -D FOREGROUND


