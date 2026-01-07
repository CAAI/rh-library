from rhnode import RHJob
import os

""" 
algorithm: Optional[str] = 'BraTs25_1'
t1: Optional[FilePath] = None
t1c: Optional[FilePath] = None
flair: Optional[FilePath] = None
t2: Optional[FilePath] = None
do_preprocess: Optional[bool] = False
preprocess_target_sequence: Optional[str] = None
resample_to_orig_spacing: Optional[bool] = False

"""

data = {
    "t1": "/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/public_glio/resliced_t1_r2s_BET.nii.gz",
    "t1c": "/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/public_glio/resliced_t1gd_r2s_BET.nii.gz",
    "t2": "/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/public_glio/resliced_t2_r2s_BET.nii.gz",
    "flair": "/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/public_glio/resliced_flair_r2s_BET.nii.gz",
    "mask": "/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/BraTs/brats25_space-publicglio_dseg.nii.gz",
}

os.makedirs('/mnt/NGGBMskanning/Analysis/dce_strid_20220520_VIDAfix/NGGBM007_NGGBM007___NGGBM007/1.3.51.0.1.1.10.143.20.159.19520054.12805853/AIsegment/BraTs', exist_ok=True)

node = RHJob(
    node_name="brats",
    manager_address="localhost:9050",
    inputs = data,
    check_cache=False,
)
node.start()
node.wait_for_finish()

