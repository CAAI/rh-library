from rhnode import RHJob

data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "t1": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T1_synth_native.nii.gz",
    "do_preprocess": False,
    #"out_filename": 'AIMS_wpreprocess.nii.gz'
    "out_filename": 'AIMS.nii.gz'
}

node = RHJob(
    node_name="aims",
    inputs = data,
    node_address = "localhost:9050",
    check_cache=False,
)

#Queue the node for execution
node.start()

# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)