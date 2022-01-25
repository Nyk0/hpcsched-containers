from kubernetes import client, config
from ClusterShell.NodeSet import NodeSet
import time
import psutil
import subprocess

def generate():
	config.load_incluster_config()
	partitions = dict()
	nodes_by_cpu = dict()
	nb_containers = 0
	v1 = client.CoreV1Api()
	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=compute-node")

	for i in ret.items:
		for containers in i.spec.containers:
			if containers.name == "slurmd":
				nb_containers += 1
				if i.metadata.labels['partition'] not in partitions.keys():
					partitions[i.metadata.labels['partition']] = NodeSet()
				partitions[i.metadata.labels['partition']].add(i.metadata.name)

				if containers.resources.requests['cpu'] not in nodes_by_cpu.keys():
					nodes_by_cpu[containers.resources.requests['cpu']] = NodeSet()
				nodes_by_cpu[containers.resources.requests['cpu']].add(i.metadata.name)

	if nb_containers == 0:
		return False

	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=control-node")

	for i in ret.items:

		for containers in i.spec.containers:
			if containers.name == "slurmctld":
				ctrl_host = i.metadata.name

	slurm_conf_file = (f"ClusterName=slurmtest\n"
	f"ControlMachine={ctrl_host}\n"
	f"SlurmUser=slurm\n"
	f"AuthType=auth/munge\n"
	f"StateSaveLocation=/var/slurm/\n"
	f"SlurmdSpoolDir=/var/slurm/\n"
	f"SlurmctldPidFile=/var/slurm/slurmctld.pid\n"
	f"SlurmdPidFile=/var/slurm/slurmd.pid\n"
	f"SlurmdLogFile=/var/slurm/slurmd.log\n"
	f"SlurmctldLogFile=/var/slurm/slurmctld.log\n"
	f"#SlurmctldParameters=enable_configless,cloud_dns\n"
	f"SlurmctldParameters=enable_configless\n"
	f"#CommunicationParameters=NoAddrCache\n"
	f"ProctrackType=proctrack/linuxproc\n")

	for cpu in nodes_by_cpu.keys():
		#slurm_conf_file = slurm_conf_file + "\nNodeName=" + str(nodes_by_cpu[cpu]) + " Procs=" + cpu + " Feature=cloud State=CLOUD"
		slurm_conf_file = slurm_conf_file + "\nNodeName=" + str(nodes_by_cpu[cpu]) + " Procs=" + cpu + " State=UNKNOWN"

	for partition in partitions.keys():
		slurm_conf_file = slurm_conf_file + "\nPartitionName=" + partition + " Nodes=" + str(partitions[partition]) + " Default=YES MaxTime=INFINITE State=UP"

	return slurm_conf_file

def write_conf(var,path):
	f = open(path,'w')
	for line in var.splitlines():
		f.write(line + "\n")
	f.close

def get_slurmctld_pid():
	process_name = "slurmctld"
	pid = 0
	for proc in psutil.process_iter():
		if process_name in proc.name():
			pid = proc.pid
	return pid

if __name__ == '__main__':
	old = False
	while True:
		current = generate()
		if old != current and current != False :
			write_conf(current,"/etc/slurm/slurm.conf")
			old = current
			if get_slurmctld_pid() > 0:
				process = subprocess.Popen(["/restart-slurm.sh"])
				process.wait()
				old = current
