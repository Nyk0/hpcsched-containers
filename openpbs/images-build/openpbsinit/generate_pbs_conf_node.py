from kubernetes import client, config
import socket
import time
import subprocess

def locate_db():
	db_server = False
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=control-node")

	for i in ret.items:
		for containers in i.spec.containers:
			if containers.name == "openpbs-server":
				db_server = i.metadata.name
	return db_server

def generate(db_server):
	oar_conf_file = (f'PBS_SERVER=' + db_server + '\n'
	f'PBS_START_SERVER=0\n'
	f'PBS_START_SCHED=0\n'
	f'PBS_START_COMM=0\n'
	f'PBS_START_MOM=1\n'
	f'PBS_EXEC=/opt/pbs\n'
	f'PBS_HOME=/var/spool/pbs\n'
	f'PBS_CORE_LIMIT=unlimited\n'
	f'PBS_SCP=/usr/bin/scp')

	return oar_conf_file

def write_conf(var,path):
	f = open(path,'w')
	for line in var.splitlines():
		f.write(line + "\n")
	f.close

if __name__ == '__main__':
	db_server = False

	while db_server == False:
		db_server = locate_db()

	write_conf(generate(db_server),"/pbsconf/pbs.conf")
