#!/bin/bash

rm -f /oarconf/oar.conf
python generate_oar_conf.py

DB_SERVER=`grep DB_HOSTNAME /oarconf/oar.conf | cut -f 2 -d '"'`

while true
do
	pg_isready -h $DB_SERVER -p 5432
	if [ $? == 0 ]
	then
		break
	fi
	sleep 2
done	

while true
do
	oar-database --create --db-admin-user root --db-admin-pass azerty --db-ro-user oar_ro --db-ro-pass azerty --conf /oarconf/oar.conf
	if [ $? == 0 ]
	then
		break
	fi
	sleep 2
done	
