from rhnode import RHJob
import shutil, os

if os.path.exists('synthmorph'):
    shutil.rmtree('synthmorph', ignore_errors=True)

data = {
    "moving_file": "/depict/data/mrac/rawdata/sub-ujUE0rikOH/ses-20160301/anat/sub-ujUE0rikOH_ses-20160301_acq-ld_rec-h19s_ct.nii.gz",
    "fixed_file": "/depict/data/mrac/rawdata/sub-ujUE0rikOH/ses-20160301/anat/sub-ujUE0rikOH_ses-20160301_t1.nii.gz",
    "moved_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_ct.nii.gz",
    "trans_file": "sub-ujUE0rikOH_ses-20160301_reg-t1_ct.reg.nii.gz",
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
