from rhnode import RHJob

data = {
    #"PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/PET_affine_BET.nii.gz",
    
    #"PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/PET.nii.gz",
    #"CT_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz",
    
    "PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0023/PET.nii.gz",
    "MRI_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0023/ANAT.nii.gz",
    
}

node = RHJob(
    node_name="amyloidai",
    inputs = data,
    node_address="titan6.petnet.rh.dk:8010",
    #node_address = "localhost:8010",
    check_cache=False,
    output_directory=".",
)

#Queue the node for execution
node.start()

# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)