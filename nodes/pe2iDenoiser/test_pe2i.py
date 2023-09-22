from rhnode import RHJob
import os, shutil

#SERVER='titan6:9030'
SERVER='localhost:9050'

""" 5pct PET """
data = {
    "pet": "/home/claes/projects/LowdosePET/PE2I/data_Vision/nii/5WJRJfMZHM_0_TEST/PETLD5pct.nii.gz",
    "ct": "/home/claes/projects/LowdosePET/PE2I/data_Vision/nii/5WJRJfMZHM_0_TEST/ACCT.nii.gz",
    "scaling_factor": 20,
    "out_filename": 'denoised.nii.gz',
}
node_5pct = RHJob(
    node_name="pe2idenoiser",
    inputs = data,
    manager_address = SERVER
)
#Queue the node for execution
node_5pct.start()

output = node_5pct.wait_for_finish()
print(output)




#####




# data = {
#     "pet": "/home/claes/projects/LowdosePET/PE2I/data_Vision/nii/5WJRJfMZHM_0/PETLD5pct_to_avg_BET_176x176x200_DC_pNORM.nii.gz",
#     "out_filename": 'denoised_MNI.nii.gz',
# }
# node_5pct = RHJob(
#     node_name="pe2idenoiser",
#     inputs = data,
#     manager_address = SERVER
# )
# #Queue the node for execution
# node_5pct.start()

# output = node_5pct.wait_for_finish()
# print(output)
