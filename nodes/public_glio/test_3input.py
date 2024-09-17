from rhnode import RHJob

data = {
    "t1c": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/resliced_CT1.nii.gz",
    "flair": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/resliced_FLAIR.nii.gz",
    "t2": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/resliced_T2.nii.gz"
}

node = RHJob(
    node_name="public_glio",
    inputs=data,
    #manager_address="aims:9030",
    #node_address='localhost:9050',
    node_address='localhost:8010',
    check_cache=False
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# Alternatively to interrupt the job:
# node.stop()
