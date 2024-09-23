from rhnode import RHJob

data = {
    "in_file": "/depict/data/ventricles/rawdata/sub-PAT001/ses-20210824/anat/sub-PAT001_ses-20210824_FLAIR.nii.gz",
}

node = RHJob(
    node_name="synthseg",
    inputs=data,
    manager_address="aims:9030",
    #node_address='localhost:9050',
    check_cache=False
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# Alternatively to interrupt the job:
# node.stop()