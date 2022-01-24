#!/bin/bash

export SLURM_CONF=/etc/slurm/slurm.conf

kill -TERM `cat /var/slurm/slurmctld.pid`
sleep 3
scontrol reconfig
