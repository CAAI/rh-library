from rhnode import RHJob
import shutil, os

# REGISTER

data = {
    "moving_file": "testdata/CT2mm.nii.gz",
    "fixed_file": "testdata/T12mm.nii.gz",
    "command": "register",
    "moved_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_ct.nii.gz",
    "trans_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_ct.reg.lta",
    "xargs": '-m rigid'
}
node = RHJob(
    node_name="synthmorph",
    inputs = data,
    #manager_address="olsen.petnet.rh.dk:9030",
    node_address="localhost:9050",
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)

# APPLY

data = {
    "moving_file": "testdata/CT2mm.nii.gz",
    "init_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_ct.reg.lta",
    "command": "apply",
    "moved_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_applied_ct.nii.gz",
}
node = RHJob(
    node_name="synthmorph",
    inputs = data,
    #manager_address="olsen.petnet.rh.dk:9030",
    node_address="localhost:9050",
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
