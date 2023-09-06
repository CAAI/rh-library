from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import subprocess
import os

class TotalSegmentatorInput(BaseModel):
    in_file:FilePath
    fast:Optional[bool]=False
    roi_subset:Optional[str]=""

class TotalSegmentatorOutput(BaseModel):
    output_directory:FilePath

class HDBetNode(RHNode):
    input_spec = TotalSegmentatorInput
    output_spec = TotalSegmentatorOutput
    name = "totalsegmentator"
    required_gb_gpu_memory = 12
    required_num_threads = 2
    required_gb_memory = 12    

    def process(inputs, job):
        out_dir = job.directory

        cmd = ["TotalSegmentator", "-i", str(inputs.in_file), "-o", str(out_dir)]
        
        if inputs.fast:
            cmd += ['--fast']
        
        if not inputs.roi_subset == "":
            cmd += ['--roi_subset',inputs.roi_subset]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        _ = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return TotalSegmentatorOutput(output_directory=out_dir)

app = HDBetNode()
