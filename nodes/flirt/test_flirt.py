from rhnode import RHJob

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT_smoothed_0-100_crop_BET.nii.gz",
    "ref_file": "/homes/claes/projects/amyloidClassifier/Data/avg_template.nii.gz",
    "omat_file": "flirt_omat.mat",
    #"out_file": "flirt_out.nii.gz"
}
node = RHJob(
    node_name="flirt",
    inputs = data,
    manager_address='titan6:9050',
    #check_cache=False,
    #save_to_cache=False,
)
node.start()
output = node.wait_for_finish()
print(output)

""" RESAMPLE """

data_resample = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT_smoothed_0-100_crop_BET.nii.gz",
    "ref_file": "/homes/claes/projects/amyloidClassifier/Data/avg_template.nii.gz",
    'init_file': 'flirt/flirt_omat.mat',
    'out_file': 'flirt_resampled.nii.gz',
    'applyxfm': True
}
node = RHJob(
    node_name="flirt",
    inputs = data_resample,
    manager_address='titan6:9050',
    #check_cache=False,
    #save_to_cache=False,
)
node.start()
output = node.wait_for_finish()
print(output)
