from rhnode import RHJob

data = {
    #"in_file": "/homes/claes/projects/LowdosePET/Cu64DOTATATE/Data/mnc/DOTA_000/CT.nii",
    "in_file": "/homes/claes/projects/LowdosePET/PE2I/data_Vision/nii/0rCyjRXXbm_0/ACCT.nii.gz",
    'fast': True,
    'roi_subset': 'brain face',
    #'out_segmentation': 'test.nii.gz'
}

node = RHJob(
    node_name="totalsegmentator",
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