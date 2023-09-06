from rhnode import RHJob
import os, shutil

shutil.rmtree('brainpetnr', ignore_errors=True)
shutil.rmtree('brainpetnr_1', ignore_errors=True)
shutil.rmtree('brainpetnr_2', ignore_errors=True)
shutil.rmtree('brainpetnr_3', ignore_errors=True)

SERVER='titan6:9030'

""" 5pct PET """
data = {
    "pet": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/PET_2mm_LD5pct.nii.gz",
    "ct": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/CT.nii.gz",
    "scaling_factor": 20,
    "out_filename": 'denoised.nii.gz',
    "model": 'PiB'
}
node_5pct = RHJob(
    node_name="brainpetnr",
    inputs = data,
    #node_address = "localhost:9050",
    #node_address = "172.16.189.243:9050",
    manager_address = SERVER
)
#Queue the node for execution
node_5pct.start()

""" 1min PET """
data = {
    "pet": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/PET_2mm_LD60sec570delay.nii.gz",
    "ct": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/CT.nii.gz",
    "scaling_factor": 1.382421726720623,
    "out_filename": 'denoised.nii.gz',
    "model": 'PiB'
}
node_1min = RHJob(
    node_name="brainpetnr",
    inputs = data,
    #node_address = "localhost:9050",
    #node_address = "172.16.189.243:9050",
    manager_address = SERVER
)
#Queue the node for execution
node_1min.start()

""" 5min PET """
data = {
    "pet": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/PET_2mm_LD300sec600delay.nii.gz",
    "ct": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/CT.nii.gz",
    "scaling_factor": 1.406185725466096,
    "out_filename": 'denoised.nii.gz',
    "model": 'PiB_5min'
}
node_5min = RHJob(
    node_name="brainpetnr",
    inputs = data,
    #node_address = "localhost:9050",
    #node_address = "172.16.189.243:9050",
    manager_address = SERVER
)
#Queue the node for execution
node_5min.start()

""" 5min PET WITH PREPROCESSING ALREADY DONE """
""" MISSING PET FILE RIGHT NOW
data = {
    "pet": "/homes/claes/projects/github/CAAI/brainPETNR/data/PiB_002_000/PET_2mm_LD300sec600delay_to_avg_BET.nii.gz",
    "scaling_factor": 1.406185725466096,
    "out_filename": 'denoised_MNI_space.nii.gz',
    "model": 'PiB_5min'
}
node = RHJob(
    node_name="brainpetnr",
    inputs = data,
    #node_address = "localhost:9050",
    #node_address = "172.16.189.243:9050",
    manager_address = SERVER
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('brainpetnr_3/denoised_MNI_space.nii.gz')
#shutil.rmtree('brainpetnr_3', ignore_errors=True)
"""

## GATHER ALL RESULTS
output_5pct = node_5pct.wait_for_finish()
print(output_5pct)
assert os.path.exists('brainpetnr/denoised.nii.gz')
#shutil.rmtree('brainpetnr', ignore_errors=True)

output_1min = node_1min.wait_for_finish()
print(output_1min)
assert os.path.exists('brainpetnr_1/denoised.nii.gz')
#shutil.rmtree('brainpetnr', ignore_errors=True)

output_5min = node_5min.wait_for_finish()
print(output_5min)
assert os.path.exists('brainpetnr_2/denoised.nii.gz')
#shutil.rmtree('brainpetnr_2', ignore_errors=True)