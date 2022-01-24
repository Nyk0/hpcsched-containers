#!/bin/bash

/opt/pbs/libexec/pbs_habitat
su - postgres -c '/usr/lib/postgresql/13/bin/postgres -D /var/spool/pbs/datastore -p 15007'
