from rhnode import RHJob
import shutil, os

data = {
    "mr": "/homes/hinge/Projects/rh-node/tests/data/mr.nii.gz"
}
node = RHJob(
    node_name="hdbet",
    inputs = data,
)
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('hdbet/mr_BET.nii.gz')
assert os.path.exists('hdbet/mr_BET_mask.nii.gz')
shutil.rmtree('hdbet', ignore_errors=True)



data = {
    "mr": "/homes/hinge/Projects/rh-node/tests/data/mr.nii.gz",
    "out_file": "MRI_bet.nii.gz"
}
node = RHJob(
    node_name="hdbet",
    inputs = data,
)
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('hdbet/MRI_bet.nii.gz')
assert os.path.exists('hdbet/MRI_bet_mask.nii.gz')
shutil.rmtree('hdbet', ignore_errors=True)