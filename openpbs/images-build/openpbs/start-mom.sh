#!/bin/bash

source /etc/profile.d/pbs.sh

PBS_CONTROLLER=`grep PBS_SERVER /etc/pbs.conf | cut -d "=" -f 2`

reach_slurmctld=1
while [ $reach_slurmctld != 0 ]
do
	nc -z $PBS_CONTROLLER 15001 > /dev/null 2>&1
	reach_slurmctld=$?
done

/opt/pbs/sbin/pbs_mom -N
