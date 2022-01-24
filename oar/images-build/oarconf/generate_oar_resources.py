from kubernetes import client, config
import subprocess
import time

def get_nodes():
	config.load_incluster_config()
	v1 = client.CoreV1Api()
	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=compute-node")
	nodes = dict()

	for i in ret.items:
		for containers in i.spec.containers:
			if containers.name == "oar-node":
				nodes[i.metadata.name] = containers.resources.requests['cpu']
	return nodes

if __name__ == '__main__':

	previous = dict()
	current = dict()
	add = dict()
	suppr = dict()

	cmd = ['/init_node.sh']
	subprocess.Popen(cmd).wait() 

	while True:
		
		current = get_nodes()
		add = {k:v for k,v in current.items() if k not in previous}
		suppr = {k:v for k,v in previous.items() if k not in current}
		if len(add) != 0 or len(suppr) != 0:
			print("add : " + str(add))
			for node in add.keys():
				cmd = ['/add_node.sh', node, add[node]]
				subprocess.Popen(cmd).wait() 
			print("suppr : " + str(suppr))
			for node in suppr.keys():
				cmd = ['/del_node.sh', node]
				subprocess.Popen(cmd).wait() 
			previous = current
		time.sleep(2)
