from rhnode import RHJob

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