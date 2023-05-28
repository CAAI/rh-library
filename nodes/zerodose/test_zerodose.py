from rhnode import RHJob

data = {
    "pet": "/homes/hinge/Projects/rh-node/tests/data/mr.nii.gz",
    "mr": "/homes/hinge/Projects/rh-node/tests/data/mr.nii.gz"
}

node = RHJob(
    node_name="zerodose",
    #node_adress="localhost:8009",
    inputs = data,
)
node.start()
node.wait_for_finish()

