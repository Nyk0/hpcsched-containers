#!/bin/bash

chown slurm:slurm /var/slurm
chmod 755 /var/slurm

while [ ! -f /etc/slurm/slurm.conf ]
do
  echo "Waiting for /etc/slurm/slurm.conf"
  sleep 2
done

slurmctld -D -f /etc/slurm/slurm.conf
