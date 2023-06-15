from rhnode import RHJob
import os, shutil

# Inputs to HDCTBET
data = {
    "ct": "/homes/claes/projects/CTBET/imagesTs/FET_004_0000.nii.gz"
}
node = RHJob(
    node_name="hdctbet",
    inputs = data,
)
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('hdctbet/FET_004_0000_BET.nii.gz')
assert os.path.exists('hdctbet/FET_004_0000_BET_mask.nii.gz')
shutil.rmtree('hdctbet', ignore_errors=True)

data = {
    "ct": "/homes/claes/projects/CTBET/imagesTs/FET_004_0000.nii.gz",
    "out_file": "CT_bet.nii.gz"
}
node = RHJob(
    node_name="hdctbet",
    inputs = data,
)
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('hdctbet/CT_bet.nii.gz')
assert os.path.exists('hdctbet/CT_bet_mask.nii.gz')
shutil.rmtree('hdctbet', ignore_errors=True)