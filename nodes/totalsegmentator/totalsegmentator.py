from rhnode import RHNode
from pydantic import BaseModel, FilePath, DirectoryPath
from typing import Optional
import subprocess
import os
import nibabel as nib


class TotalSegmentatorInput(BaseModel):
    in_file:FilePath
    fast:Optional[bool]=False
    roi_subset:Optional[str]=""
    task:str="total"
    body_seg:Optional[bool]=False
    force_split:Optional[bool]=False
    remove_small_blobs:Optional[bool]=False
    output_type:Optional[str]='nifti'
    
class TotalSegmentatorOutput(BaseModel):
    out_segmentation:FilePath
    out_version:str
    out_args:str

class TotalSegmentatorNode(RHNode):
    input_spec = TotalSegmentatorInput
    output_spec = TotalSegmentatorOutput
    name = "totalsegmentator"
    required_gb_gpu_memory = 12
    required_num_threads = 2
    required_gb_memory = 12    

    def process(inputs:TotalSegmentatorInput, job) -> TotalSegmentatorOutput:
        out_file = job.directory / 'segmentation.nii.gz'

        cmd = ["TotalSegmentator", "-i", str(inputs.in_file), "-o", str(out_file), "-ta", inputs.task]

        cmd_args = ["--ml"]
        
        if inputs.fast:
            cmd_args += ['--fast']
        if inputs.body_seg:
            cmd_args += ['--body_seg']
        if inputs.force_split:
            cmd_args += ['--force_split']
        if inputs.remove_small_blobs:
            cmd_args += ['--remove_small_blobs']
        if inputs.output_type == 'dicom':
            cmd_args += ['--output_type', 'dicom']
            
        #shape = nib.load(str(inputs.in_file)).shape
        # if shape[-1] > 590:
        #     print("Large image, running with --body_seg --force_split --nr_thr_saving 1")
        #     cmd_args+=["--body_seg","--force_split","--nr_thr_saving","1"]

        if not inputs.roi_subset == "":
            cmd_args += ['--roi_subset'] + inputs.roi_subset.split(" ")

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        
        print("TOTALSEGMENTATOR STARTING VERSION")
        version = subprocess.check_output("TotalSegmentator --version".split(" "),env=all_env_vars)        
        print("TOTALSEGMENTATOR STARTING SEGMENTATION")
        out = subprocess.check_output(cmd+cmd_args, text=True,env=all_env_vars)
        print("TOTALSEGMENTATOR ENDING")

        return TotalSegmentatorOutput(out_segmentation=out_file,out_version=version,out_args=" ".join(cmd_args))

app = TotalSegmentatorNode()
