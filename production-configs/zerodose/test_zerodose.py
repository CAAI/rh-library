from rhnode import NodeRunner, new_job

data = {
    "pet": "/homes/hinge/Projects/rh-node/test/mr.nii.gz",
    "mr": "/homes/hinge/Projects/rh-node/test/mr.nii.gz"
}

job = new_job(check_cache=False)

node = NodeRunner(
    identifier="zerodose",
    manager_adress="peyo:9050",
    inputs = data,
    job = job,
)
node.start()
node.wait_for_finish()

