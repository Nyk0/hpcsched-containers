#!/bin/bash

oarnodesetting -h $1 -s Dead

for r_id in `oarnodes --sql "network_address = '$1'" | grep "resource_id" | cut -f 2 -d ":" | sed -r 's/( )+//g'`
do
	oarremoveresource $r_id
done
