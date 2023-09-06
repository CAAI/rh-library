from rhnode import RHJob
import os, shutil

data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "t1": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T1_synth_native.nii.gz",
    "out_filename": 'AIMS_wpreprocess.nii.gz',
    'do_preprocess': True
}
node = RHJob(
    node_name="aims",
    inputs = data,
    #node_address = "localhost:9050",
    node_address = "aims:9030",
    check_cache=False,
)
#Queue the node for execution
node.start()
output = node.wait_for_finish()
print(output)
assert os.path.exists('aims/AIMS_wpreprocess.nii.gz')
assert os.path.exists('aims/FLAIR_preprocessed.nii.gz')
assert os.path.exists('aims/T2_preprocessed.nii.gz')
assert os.path.exists('aims/T1_preprocessed.nii.gz')
shutil.rmtree('aims', ignore_errors=True)

data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "t1": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T1_synth_native.nii.gz",
    "do_preprocess": False,
    "out_filename": 'AIMS.nii.gz'
}
node = RHJob(
    node_name="aims",
    inputs = data,
    #node_address = "localhost:9050",
    node_address = "aims:9030",
    check_cache=False,
)
#Queue the node for execution
node.start()
# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)
assert os.path.exists('aims/AIMS.nii.gz')
shutil.rmtree('aims', ignore_errors=True)

## WITH orig MODEL
data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "t1": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T1_synth_native.nii.gz",
    "do_preprocess": False,
    "model_name": 'FLAIR_T2_T1_orig',
    "out_filename": 'AIMS.nii.gz'
}
node = RHJob(
    node_name="aims",
    inputs = data,
    #node_address = "localhost:9050",
    node_address = "aims:9030",
    check_cache=False,
)
#Queue the node for execution
node.start()
# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)
assert os.path.exists('aims/AIMS.nii.gz')
shutil.rmtree('aims', ignore_errors=True)


## With no T1 model
data = {
    "flair": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/FLAIR_synth_native.nii.gz",
    "t2": "/homes/claes/projects/testarea/MS_SyntheticLesions/Data/training_data/MSSEG_13322/T2_synth_native.nii.gz",
    "do_preprocess": False,
    "model_name": 'FLAIR_T2_orig',
    "out_filename": 'AIMS.nii.gz'
}
node = RHJob(
    node_name="aims",
    inputs = data,
    #node_address = "localhost:9050",
    node_address = "aims:9030",
    check_cache=False,
)
#Queue the node for execution
node.start()
# Saves files in cwd/node_name_[i]/}
output = node.wait_for_finish()
print(output)
assert os.path.exists('aims/AIMS.nii.gz')
shutil.rmtree('aims', ignore_errors=True)