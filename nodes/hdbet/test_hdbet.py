from rhnode import RHJob

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