from rhnode import RHJob
import shutil, os

if os.path.exists('convertxfm'):
    shutil.rmtree('convertxfm', ignore_errors=True)

"""
data = {
    "in_file": ".mat",
    "inverse": True,
    "out_file": "ANAT_std.nii.gz"
}
node = RHJob(
    node_name="convertxfm",
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
assert os.path.exists('convertxfm/ANAT_std.nii.gz')
"""