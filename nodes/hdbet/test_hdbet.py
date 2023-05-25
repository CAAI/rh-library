from rhnode import NodeRunner, new_job

# Steps:
# 1. Define the inputs to the node you wish to run
# 2. Define the job parameters (priority, whether to check cache)
# 3. Start the node with NodeRunner
# 4. Either wait for the node to finish or stop the node

# Inputs to HDBET
data = {
    "mr": "/homes/hinge/Projects/rh-node/test/mr.nii.gz"
}

# JOB parameters
#new_job parameters:
#   check_cache=True - If true, will return the cached result if it exists
#   save_to_cache=True - If true, will save the result to the cache. 
#   priority=[1..5]
#   name="job_name"


### NodeRunner other arguments
#   output_directory=... - Where to save the output. Default is cwd/node_name_[i]/}
#   manager_adress=... - Where to find the manager node. Default is localhost:9050
#   host=... - Hostname of the task node. Default is to ask manager where to run
#   port=... - Port of the task node. Default is to ask manager where to run

# NOTE: manager_adress and host/port are mutually exclusive.

nodes = []
for _ in range(10):
    job = new_job(check_cache=False) 
    node = NodeRunner(
        identifier="hdbet",
        inputs = data,
        manager_adress="titan6:9050",
        job = job,
    )

    #Queue the node for execution
    node.start()

    #Save a reference to the node
    nodes.append(node)

# wait for each node to finish and save the output
for node in nodes:
    
    # Saves files in cwd/node_name_[i]/}
    output = node.wait_for_finish()
    print(output)


# check the status of the node in the manager queue at http://hostname:9050/manager
# check the status of the node job at http://hostname:9050/{identifier}

# alternatively, stop all the nodes 
#
# for node in nodes:
#     node.stop()
