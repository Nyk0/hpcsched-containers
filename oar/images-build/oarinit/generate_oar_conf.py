from kubernetes import client, config
import socket
import time
import subprocess

def locate_db():
	db_server = False
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=db-node")

	for i in ret.items:
		for containers in i.spec.containers:
			if containers.name == "postgres":
				db_server = i.metadata.name
	return db_server

def generate(db_server):
	oar_conf_file = (f'DB_TYPE="Pg"\n'
	f'DB_HOSTNAME=\"' + db_server + '\"\n'
	f'DB_PORT="5432"\n'
	f'DB_BASE_NAME="oar"\n'
	f'DB_BASE_LOGIN="oar"\n'
	f'DB_BASE_PASSWD="azerty"\n'
	f'DB_BASE_LOGIN_RO="oar_ro"\n'
	f'DB_BASE_PASSWD_RO="azerty"\n'
	f'SERVER_HOSTNAME="localhost"\n'
	f'SERVER_PORT="6666"\n'
	f'OARSUB_DEFAULT_RESOURCES="/resource_id=1"\n'
	f'OARSUB_NODES_RESOURCES="network_address"\n'
	f'OARSUB_FORCE_JOB_KEY="no"\n'
	f'LOG_LEVEL="3"\n'
	f'LOG_CATEGORIES="all"\n'
	f'OAREXEC_DEBUG_MODE="1"\n'
	f'OAR_RUNTIME_DIRECTORY="/var/lib/oar"\n'
	f'LOG_FILE="/var/log/oar.log"\n'
	f'DEPLOY_HOSTNAME="127.0.0.1"\n'
	f'COSYSTEM_HOSTNAME="127.0.0.1"\n'
	f'DETACH_JOB_FROM_SERVER="1"\n'
	f'OPENSSH_CMD="/usr/bin/ssh -p 6667 -e none"\n'
	f'FINAUD_FREQUENCY="0"\n'
	f'#FINAUD_FREQUENCY="300"\n'
	f'PINGCHECKER_SENTINELLE_SCRIPT_COMMAND="/usr/lib/oar/sentinelle.pl -t 30 -w 20"\n'
	f'SCHEDULER_TIMEOUT="30"\n'
	f'SCHEDULER_NB_PROCESSES=1\n'
	f'SCHEDULER_JOB_SECURITY_TIME="60"\n'
	f'SCHEDULER_GANTT_HOLE_MINIMUM_TIME="300"\n'
	f'SCHEDULER_RESOURCE_ORDER="scheduler_priority ASC, state_num ASC, available_upto DESC, suspended_jobs ASC, network_address ASC, resource_id ASC"\n'
	f'SCHEDULER_RESOURCE_ORDER_ADV_RESERVATIONS="network_address ASC, resource_id ASC"\n'
	f'SCHEDULER_PRIORITY_HIERARCHY_ORDER="network_address/resource_id"\n'
	f'SCHEDULER_AVAILABLE_SUSPENDED_RESOURCE_TYPE="default"\n'
	f'SCHEDULER_FAIRSHARING_MAX_JOB_PER_USER=30\n'
	f'ENERGY_SAVING_INTERNAL="no"\n'
	f'JOB_RESOURCE_MANAGER_PROPERTY_DB_FIELD="cpuset"\n'
	f'JOB_RESOURCE_MANAGER_FILE="/etc/oar/job_resource_manager_cgroups.pl"\n'
	f'#CPUSET_PATH="/oar"\n'
	f'OARSH_OARSTAT_CMD="/usr/bin/oarstat"\n'
	f'OPENSSH_OPTSTR="1246ab:c:e:fgi:kl:m:no:p:qstvxAB:CD:E:F:GI:J:KL:MNO:PQ:R:S:TVw:W:XYy"\n'
	f'OPENSSH_OPTSTR_FILTERED="1246b:c:fm:nqstvxBCNPQ:TVXYy"\n'
	f'OARSH_OPENSSH_DEFAULT_OPTIONS="-e none -oProxyCommand=none -oPermitLocalCommand=no -oUserKnownHostsFile=/var/lib/oar/.ssh/known_hosts"\n'
	f'OARSTAT_DEFAULT_OUTPUT_FORMAT=2')

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

	write_conf(generate(db_server),"/oarconf/oar.conf")
