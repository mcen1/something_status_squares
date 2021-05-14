#!/bin/bash
MYRC=0

ps -ef | grep -v grep | grep apache
if [ $? -ne 0 ]; then
  MYRC=1
  echo "Apache is not running."
fi
exit $MYRC
