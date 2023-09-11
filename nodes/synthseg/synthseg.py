from rhnode import RHNode
from pydantic import BaseModel, FilePath, DirectoryPath
from typing import Optional
import subprocess
import os

class SynthSegInput(BaseModel):
    in_file:FilePath
    xargs:Optional[str]=""

class SynthSegOutput(BaseModel):
    out_segmentation:FilePath

class SynthSegNode(RHNode):
    input_spec = SynthSegInput
    output_spec = SynthSegOutput
    name = "synthseg"
    required_gb_gpu_memory = 12
    required_num_threads = 2
    required_gb_memory = 12    

    def process(inputs, job):
        out_file = job.directory / 'segmentation.nii.gz'

        cmd = ["python", "./scripts/commands/SynthSeg_predict.py", "--i", str(inputs.in_file), "--o", str(out_file)]
        
        if not inputs.xargs == "":
            cmd += inputs.xargs.split(' ')

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        out = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return SynthSegOutput(out_segmentation=out_file)

app = SynthSegNode()
