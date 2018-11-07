import time
import ray
import os

def create_worker_devcloud(n_workers):
    # Stop any existing servers
    os.system('ray stop')

    # Clean up existing workers/temp files
    #os.system('rm -f STDIN.*')
    os.system('rm -f start_ray_worker*')

    # Find any current worker jobs and remove them
    #os.system('/usr/local/bin/qstat | grep start_ray_worker | cut -f 1 -d ' ' | xargs /usr/local/bin/qdel')

    # Wait until qdel removes any ray worker jobs
    #time.sleep(1)
    print("Got to 1")

    # Display all jobs in the queue
    # There should only be one job running in the jupyterhub queue
    #os.system('qstat')

    # Write the Ray head node commands to start_ray
    with open('start_ray','w') as f:
        f.write("ray start --head --redis-port=6380\n")

    # Start Ray head node on current node
    #os.system('nohup bash start_ray')
    os.system('bash start_ray')
    time.sleep(3)
    
    ray.init("localhost:6380")
    
    # Wait for the head node to start
    time.sleep(3)

    # Spawn worker process on remote nodes, time limit defaults to 1 hour but is adjustable
    with open('start_ray_worker','w') as f:
        f.write("/glob/intel-python/versions/2018u2/intelpython3/bin/python ~/.local/bin/ray start --redis-address='localhost':6380; sleep 3600\n")

    #Call start_ray_worker multiple times for more nodes (5 max)
    for _ in range(n_workers):
        os.system('/usr/local/bin/qsub start_ray_worker')
           
    #time.sleep(10)
    print("Got to 2")
    
    #ray.init()
    #ray.init("localhost:6380")

    print("Got to 3")

    @ray.remote
    def f():
        time.sleep(0.01)
        #os.system('/usr/local/bin/qstat')
        return ray.services.get_node_ip_address()

    # Get a list of the IP addresses of the nodes that have joined the cluster.
    # There should be (n_workers + 1) ip addresses (head node + worker nodes)
    # In the default example of 2 worker nodes, there should be 3 ip addresses
    ips = []
    while len(ips) != n_workers+1:
        os.system('/usr/local/bin/qstat')
        ips = set(ray.get([f.remote() for _ in range(1000)]))
        print(ips)
        time.sleep(1)

    return ips
