from rhnode import NodeRunner, new_job

# Steps:
# 1. Define the inputs to the node you wish to run
# 2. Define the job parameters (priority, whether to check cache)
# 3. Start the node with NodeRunner
# 4. Either wait for the node to finish or stop the node

# Inputs to HDCTBET
data = {
    "ct": "/homes/claes/projects/CTBET/imagesTs/FET_004_0000.nii.gz"
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

job = new_job(check_cache=False) 
job.device=0
node = NodeRunner(
    identifier="hdctbet",
    inputs = data,

    #manager_adress="titan6.petnet.rh.dk:8010",
    host='titan6.petnet.rh.dk',
    port=8010,
    resources_included=True,

    job = job,
)

#Queue the node for execution
node.start()

   
# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)

# check the status of the node in the manager queue at http://hostname:9050/manager
# check the status of the node job at http://hostname:9050/{identifier}

# alternatively, stop all the nodes 
# node.stop()
