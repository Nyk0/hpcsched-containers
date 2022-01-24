#!/bin/bash

i=1
while [ ! $i -gt $2 ]
do
	oarnodesetting -a -h $1 -p host=hpc-node-0 -p cpu=1 -p core=$i
	((i++))
done
