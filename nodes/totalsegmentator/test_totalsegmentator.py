from rhnode import RHJob

data = {
    "in_file": "/homes/claes/projects/LowdosePET/Cu64DOTATATE/Data/mnc/DOTA_000/CT.nii",
    'fast': True,
    'roi_subset': 'spleen liver heart_myocardium brain gluteus_maximus_left gluteus_maximus_right',
    'output_directory': 'segmn_test'
}

node = RHJob(
    node_name="totalsegmentator",
    inputs=data,
    node_address="localhost:9050",
    resources_included=True,
    included_cuda_device=0,  # if applicable
    priority=3,
    check_cache=False,
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()

# Alternatively to interrupt the job:
# node.stop()