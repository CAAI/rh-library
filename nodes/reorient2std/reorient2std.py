from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess


class Reorient2stdInputs(BaseModel):
    in_file: FilePath
    out_file: str = None


class Reorient2stdOutputs(BaseModel):
    out: FilePath = None
    out_message: str


class Reorient2stdNode(RHNode):
    input_spec = Reorient2stdInputs
    output_spec = Reorient2stdOutputs
    name = "reorient2std"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        outpath = job.directory / inputs.out_file
        
        cmd = ["fslreorient2std",
               str(inputs.in_file),
               str(outpath)]

        all_env_vars = os.environ.copy()
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)
    
        return Reorient2stdOutputs(out=outpath, out_message=output)


app = Reorient2stdNode()