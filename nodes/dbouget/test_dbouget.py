from rhnode import RHJob

data = {
    "in_file": "/depict/data/public_data/BraTS-MEN-RT-Train-v2/BraTS-MEN-RT-0002-1/BraTS-MEN-RT-0002-1_t1c.nii.gz",
    "segmentation": 'dbouget/segmentation.nii.gz'
}

node = RHJob(
    node_name="dbouget",
    manager_address="localhost:9050",
    inputs = data,
    check_cache=False,
)
node.start()
node.wait_for_finish()

