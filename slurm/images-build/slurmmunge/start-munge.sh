#!/bin/bash

chmod 1777 /run/munge

su -l munge -s /bin/bash -c '/usr/sbin/munged -F'
