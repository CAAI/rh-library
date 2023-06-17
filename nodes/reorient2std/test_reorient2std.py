from rhnode import RHJob
import shutil, os

if os.path.exists('reorient2std'):
    shutil.rmtree('reorient2std', ignore_errors=True)
if os.path.exists('reorient2std_1'):
    shutil.rmtree('reorient2std_1', ignore_errors=True)

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz",
    "out_file": "ANAT_std.nii.gz"
}
node = RHJob(
    node_name="reorient2std",
    inputs = data,
    manager_address='localhost:9050',
    resources_included=True,
    check_cache=False,
    save_to_cache=False,
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('reorient2std/ANAT_std.nii.gz')

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz"
}
node = RHJob(
    node_name="reorient2std",
    inputs = data,
    manager_address='localhost:9050',
    resources_included=True,
    check_cache=False,
    save_to_cache=False,
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('reorient2std_1/ANAT_r2s.nii.gz')

shutil.rmtree('reorient2std', ignore_errors=True)
shutil.rmtree('reorient2std_1', ignore_errors=True)
