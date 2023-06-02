from rhnode import RHJob

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz",
    "out_file": "ANAT_std.nii.gz"
}

node = RHJob(
    node_name="reorient2std",
    inputs = data,
    #node_address="titan6.petnet.rh.dk:8010",
    node_address="localhost:8010",
    resources_included=True,
    check_cache=False,
    save_to_cache=False,
)

#Queue the node for execution
node.start()

output = node.wait_for_finish()
print(output)
