#!/bin/bash

declare -a progs=("pbs_comm" "pbs_sched" "pbs_ds_monitor" "pbs_server.bin")

PBS_SERVER=`grep PBS_SERVER /etc/pbs.conf | cut -f 2 -d '='`

while true
do
	pg_isready -h $PBS_SERVER -p 15007
	if [ $? == 0 ]
	then
		break
	fi
	sleep 2
done

/opt/pbs/sbin/pbs_comm
/opt/pbs/sbin/pbs_sched
/opt/pbs/sbin/pbs_ds_monitor monitor
/opt/pbs/sbin/pbs_server

while true
do
	for prog in "${progs[@]}"
	do
		pidof $prog
		if [ $? -ne 0 ]
		then
			exit 1
		fi
	done
	sleep 2
done

exit 0
