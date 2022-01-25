#!/bin/bash

source /etc/profile.d/pbs.sh

qmgr -c "create node $1 resources_available.ncpus=$2"
qmgr -c "set node $1 queue=$3"
