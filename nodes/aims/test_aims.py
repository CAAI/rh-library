from rhnode import RHJob

data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "t1": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T1_synth_native.nii.gz",
    "do_preprocess": True,
    "out_filename": 'AIMS_wpreprocess.nii.gz'
}

node = RHJob(
    node_name="aims",
    inputs = data,
    #node_address="titan6.petnet.rh.dk:8010",
    #node_address = "localhost:8010",
    manager_address='titan6:9050',
    output_directory=".",
)

#Queue the node for execution
node.start()

# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)