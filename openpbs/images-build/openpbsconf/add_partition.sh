#!/bin/bash

source /etc/profile.d/pbs.sh

qmgr -c "create queue $1"
qmgr -c "set queue $1 queue_type=Execution"
qmgr -c "set queue $1 enabled=True"
qmgr -c "set queue $1 started=True"
