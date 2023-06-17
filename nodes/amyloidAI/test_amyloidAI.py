from rhnode import RHJob

data = [
    {"PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/PET_affine_BET.nii.gz"},

    {   
    "PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/PET.nii.gz",
    "CT_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz"},
    
    {"PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0023/PET_affine_BET.nii.gz"},
    {
    "PET_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0023/PET.nii.gz",
    "MRI_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0023/ANAT.nii.gz"}
]


nodes=[]
for d in data:
    node = RHJob(
        node_name="amyloidai",
        inputs = d,
        node_address='localhost:9050'
    )

    #Queue the node for execution
    node.start()
    nodes.append(node)

for ind,node in enumerate(nodes):
    output = node.wait_for_finish()
    print(data[ind]['PET_file'], output)
