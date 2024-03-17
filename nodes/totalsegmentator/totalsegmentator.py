from rhnode import RHNode
from pydantic import BaseModel, FilePath, DirectoryPath
from typing import Optional
import subprocess
import os

class TotalSegmentatorInput(BaseModel):
    in_file:FilePath
    fast:Optional[bool]=False
    roi_subset:Optional[str]=""

class TotalSegmentatorOutput(BaseModel):
    out_segmentation:FilePath

class TotalSegmentatorNode(RHNode):
    input_spec = TotalSegmentatorInput
    output_spec = TotalSegmentatorOutput
    name = "totalsegmentator"
    required_gb_gpu_memory = 15
    required_num_threads = 2
    required_gb_memory = 12    

    def process(inputs, job):
        out_file = job.directory / 'segmentation.nii.gz'

        cmd = ["TotalSegmentator", "-i", str(inputs.in_file), "-o", str(out_file), "--ml"]
        
        if inputs.fast:
            cmd += ['--fast']
        
        if not inputs.roi_subset == "":
            cmd += ['--roi_subset'] + inputs.roi_subset.split(" ")

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        out = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return TotalSegmentatorOutput(out_segmentation=out_file)

app = TotalSegmentatorNode()
