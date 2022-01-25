#!/bin/bash

source /etc/profile.d/pbs.sh

qmgr -c "delete node $1"
