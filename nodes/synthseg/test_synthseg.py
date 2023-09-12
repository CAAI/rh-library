from rhnode import RHJob

data = {
    "in_file": "/homes/claes/projects/LowdosePET/PE2I/data_Vision/nii/0rCyjRXXbm_0/ACCT.nii.gz",
    "xargs": '--ct --fast --crop 90'
}

node = RHJob(
    node_name="synthseg",
    inputs=data,
    #manager_address="aims:9030",
    node_address='localhost:9050',
    #node_address='localhost:8010',
    check_cache=False
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# Alternatively to interrupt the job:
# node.stop()