from rhnode import RHJob

data = {
    #"in_file": "/homes/claes/projects/LowdosePET/Cu64DOTATATE/Data/mnc/DOTA_000/CT.nii",
    "in_file": "/homes/hinge/lymphoma/data/raw/RIS_PACS/LM12533_02/CTres_crop.nii.gz",#"/homes/claes/projects/LowdosePET/PE2I/data_Vision/nii/0rCyjRXXbm_0/ACCT.nii.gz",
    'fast': True,
    'roi_subset': 'brain skull',
    #'out_segmentation': 'test.nii.gz'
}

node = RHJob(
    node_name="totalsegmentator",
    inputs=data,
    manager_address="titan5:9030",
    check_cache=False,
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# Alternatively to interrupt the job:
# node.stop()