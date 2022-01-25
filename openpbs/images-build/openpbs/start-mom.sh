#!/bin/bash


/opt/pbs/sbin/pbs_mom

while true
do
	pidof "pbs_mom" > /dev/null 2>&1
	if [ $? -ne 0 ]
	then
		exit 1
	fi
	sleep 2
done

exit 0
