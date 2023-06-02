from rhnode import RHJob

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT_smoothed_0-100_crop_BET.nii.gz",
    "ref_file": "/homes/claes/projects/amyloidClassifier/Data/avg_template.nii.gz",
    #"omat_file": "flirt_omat.mat",
    "out_file": "flirt_out.nii.gz"
}

data_resample = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT_smoothed_0-100_crop_BET.nii.gz",
    "ref_file": "/homes/claes/projects/amyloidClassifier/Data/avg_template.nii.gz",
    'init_file': 'flirt_5/flirt_omat.mat',
    'out_file': 'flirt_resampled.nii.gz',
    'applyxfm': True
}

node = RHJob(
    node_name="flirt",
    #inputs = data,
    inputs = data_resample,
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
