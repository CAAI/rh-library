from rhnode import RHJob

data = {
    "in_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_in.nii.gz",
    "out_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_opp.nii.gz"
}

node = RHJob(
    node_name="deepdixon_2020",
    node_address='localhost:9080',
    inputs = data,
)
node.start()
node.wait_for_finish()

