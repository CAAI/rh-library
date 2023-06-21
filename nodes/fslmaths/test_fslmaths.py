from rhnode import RHJob
import shutil, os

if os.path.exists('fslmaths'):
    shutil.rmtree('fslmaths', ignore_errors=True)

data = {
    "in_file": "/homes/claes/projects/amyloidClassifier/Data/nii/amyloid_0010/ANAT.nii.gz",
    'xargs': '-add 10',
    "out_file": "ANAT_plus_10.nii.gz"
}
node = RHJob(
    node_name="fslmaths",
    inputs = data,
    #manager_address='localhost:9050',
    manager_address='172.16.189.243:9050',
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('fslmaths/ANAT_plus_10.nii.gz')

#shutil.rmtree('fslmaths', ignore_errors=True)