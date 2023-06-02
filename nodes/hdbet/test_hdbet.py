from rhnode import RHJob

# Steps:
# 1. Define the inputs to the node you wish to run
# 2. Define the job parameters (priority, whether to check cache)
# 3. Start the node with NodeRunner
# 4. Either wait for the node to finish or stop the node

# Inputs to HDBET
data = {
    "mr": "/homes/hinge/Projects/rh-node/tests/data/mr.nii.gz"
}


# NOTE: manager_adress and host/port are mutually exclusive.

nodes = []
for _ in range(1):
    node = RHJob(
        node_name="hdbet",
        inputs = data,
        node_address="titan6.petnet.rh.dk:8010",
        check_cache=False,
        resources_included=True,
        included_cuda_device=0,
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
