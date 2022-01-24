#!/bin/bash

declare -a progs=("pbs_comm" "pbs_sched" "pbs_ds_monitor" "pbs_server.bin")

/opt/pbs/libexec/pbs_habitat

/opt/pbs/sbin/pbs_comm
/opt/pbs/sbin/pbs_sched
/opt/pbs/sbin/pbs_server

while true
do
	for prog in "${progs[@]}"
	do
		pidof $prog > /dev/null 2>&1
		if [ $? -ne 0 ]
		then
			exit 1
		fi
	done
	sleep 2
done

exit 0
