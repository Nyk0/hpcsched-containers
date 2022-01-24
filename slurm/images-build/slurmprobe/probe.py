from kubernetes import client, config
import time

def locate_slurmctld():
	config.load_incluster_config()

	v1 = client.CoreV1Api()

	ret = v1.list_namespaced_pod("hpc-nico", label_selector="role=control-node")
	for i in ret.items:
		for container in i.spec.containers:
			if container.name == "slurmctld":
				return i.metadata.name
	return False

if __name__ == '__main__':

	ctrl_host = locate_slurmctld()

	while ctrl_host == False:
		ctrl_host = locate_slurmctld()
		time.sleep(2)

	f = open("/locate/host.txt",'w')
	f.write(ctrl_host)
	f.close()
