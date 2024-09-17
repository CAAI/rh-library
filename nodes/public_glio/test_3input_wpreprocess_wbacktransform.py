from rhnode import RHJob

data = {
    "t1c": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/CT1.nii.gz",
    "flair": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/FLAIR.nii.gz",
    "t2": "/homes/claes/projects/github/DEPICT-RH/public_glio/test/T2.nii.gz",
    "do_preprocess": True,
    "resample_to_orig_spacing": True
}

node = RHJob(
    node_name="public_glio",
    inputs=data,
    manager_address="aims:9030",
    #node_address='localhost:9050',
    #node_address='localhost:8010',
    #check_cache=True
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# Alternatively to interrupt the job:
# node.stop()
