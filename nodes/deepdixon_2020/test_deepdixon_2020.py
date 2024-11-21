from rhnode import RHJob

# VB20
data = {
    "in_phase": "/depict/data/mrac/rawdata/sub-1tIv2WT0Ws/ses-20140829/anat/sub-1tIv2WT0Ws_ses-20140829_in.nii.gz",
    "out_phase": "/depict/data/mrac/rawdata/sub-1tIv2WT0Ws/ses-20140829/anat/sub-1tIv2WT0Ws_ses-20140829_opp.nii.gz",
    'mMR_version': 'B20P'
}

node = RHJob(
    node_name="deepdixon_2020",
    #node_address='localhost:9080',
    node_address='titan6:9030',
    inputs = data,
)
node.start()
node.wait_for_finish()

# VE11

data = {
    "in_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_in.nii.gz",
    "out_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_opp.nii.gz",
    'mMR_version': 'E11'
}

node = RHJob(
    node_name="deepdixon_2020",
    #node_address='localhost:9080',
    node_address='titan6:9030',
    inputs = data,
)
node.start()
node.wait_for_finish()


data = {
    "in_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_in.nii.gz",
    "out_phase": "/depict/data/mrac/rawdata/sub-2jOpUJ7SHl/ses-20201221/anat/sub-2jOpUJ7SHl_ses-20201221_opp.nii.gz",
}

node = RHJob(
    node_name="deepdixon_2020",
    #node_address='localhost:9080',
    node_address='titan6:9030',
    inputs = data,
)
node.start()
node.wait_for_finish()


