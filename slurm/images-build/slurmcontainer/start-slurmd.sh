#!/bin/bash

SLURM_CONTROLLER=`cat /locate/host.txt`

reach_slurmctld=1
while [ $reach_slurmctld != 0 ]
do
        nc -z $SLURM_CONTROLLER 6817 > /dev/null 2>&1
        reach_slurmctld=$?
done

slurmd --conf-server $SLURM_CONTROLLER:6817 -D
