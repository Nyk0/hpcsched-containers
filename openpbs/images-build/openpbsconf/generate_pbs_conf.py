from kubernetes import client, config
import subprocess
import time
import socket

nodes_to_partitions = dict()
nodes_to_cpus = dict()
partitions = []

def get_nodes():
	global nodes_to_partitions
	nodes_to_partitions = dict()
	global nodes_to_cpus
	nodes_to_cpus = dict()
	global partitions
	partitions = []
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=compute-node")
	nodes_list = []
	for i in ret.items:
		for containers in i.spec.containers:
			if containers.name == "openpbs-node":
				try:
					socket.gethostbyname(i.metadata.name)
					nodes_to_partitions[i.metadata.name] = i.metadata.labels['partition']
					nodes_to_cpus[i.metadata.name] = containers.resources.requests['cpu']
					if i.metadata.labels['partition'] not in partitions:
						partitions.append(i.metadata.labels['partition'])
				except:
					print("---------DNS failed------------")
					pass

if __name__ == '__main__':

	previous_nodes_to_cpus = dict()
	previous_partitions = []
	add_nodes = dict()
	suppr_nodes = dict()
	add_partitions = []
	suppr_partitions = []
	get_nodes()

	while True:
		add_partitions = {k for k in partitions if k not in previous_partitions}
		suppr_partitions = {k for k in previous_partitions if k not in partitions}
		if len(add_partitions) != 0 or len(suppr_partitions) != 0:
			for part in add_partitions:
				print('add part : ' + part)
				cmd = ['/add_partition.sh', part]
				subprocess.Popen(cmd).wait() 
			for part in suppr_partitions:
				print('del part : ' + part)
				cmd = ['/del_partition.sh', part]
				subprocess.Popen(cmd).wait() 
			previous_partitions = partitions
		
		add_nodes = {k:v for k,v in nodes_to_cpus.items() if k not in previous_nodes_to_cpus}
		suppr_nodes = {k:v for k,v in previous_nodes_to_cpus.items() if k not in nodes_to_cpus}
		if len(add_nodes) != 0 or len(suppr_nodes) != 0:
			for node in add_nodes.keys():
				print('add node : ' + node + ' ' + add_nodes[node] + ' ' + nodes_to_partitions[node])
				cmd = ['/add_node.sh', node, add_nodes[node], nodes_to_partitions[node]]
				subprocess.Popen(cmd).wait() 
			for node in suppr_nodes.keys():
				print('del node : ' + node)
				cmd = ['/del_node.sh', node]
				subprocess.Popen(cmd).wait() 
			previous_nodes_to_cpus = nodes_to_cpus
		get_nodes()
		time.sleep(2)
