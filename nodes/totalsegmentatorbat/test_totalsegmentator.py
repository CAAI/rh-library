#from rhnode import RHJob
from rhnode import RHJob

data = {
    #"in_file": "/homes/claes/projects/LowdosePET/Cu64DOTATATE/Data/mnc/DOTA_000/CT.nii",
    #"in_file": "/homes/hinge/Projects/rh-library/nodes/totalsegmentator/testlarge.nii.gz",#"/homes/hinge/lymphoma/data/raw/RIS_PACS/LM12533_02/CTres_crop.nii.gz",#"/homes/claes/projects/LowdosePET/PE2I/data_Vision/nii/0rCyjRXXbm_0/ACCT.nii.gz",
    "in_file": "/homes/hinge/lymphoma/data/raw/RIS_PACS/LM12533_02/CTres_crop.nii.gz",
   # 'roi_subset': 'brain skull',
   #"output_type": 'dicom',
    'out_segmentation': 'test.nii.gz',
}

node = RHJob(
    node_name="totalsegmentatorbat",
    inputs=data,
    #manager_address="olsen.petnet.rh.dk:9030",
    node_address="localhost:9050",
    check_cache=True,
    resources_included=True,
    included_cuda_device=0
)
# Wait for the node to finish
node.start()

output = node.wait_for_finish()
print(output)

# totalsegmentator(
#         str(data["in_file"]), "/homes/hinge/Projects/rh-library/nodes/totalsegmentator/out.nii.gz",ml=True, nr_thr_resamp=1, nr_thr_saving=1,
#         fast=False, nora_tag="None", preview=False, task="total", roi_subset=None,
#         statistics=False, radiomics=False, crop_path=None, body_seg=False,
#         force_split=False, output_type="nifti", quiet=False, verbose=False, test=0,
#         skip_saving=False, device="gpu", license_number=None,
#         statistics_exclude_masks_at_border=True, no_derived_masks=False,
#         v1_order=False, fastest=False, roi_subset_robust=None
# )

# Alternatively to interrupt the job:
# node.stop()
