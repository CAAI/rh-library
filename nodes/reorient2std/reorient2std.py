from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess


class Reorient2stdInputs(BaseModel):
    in_file: FilePath
    out_file: Optional[str] = None
    output_matrix: Optional[bool] = False


class Reorient2stdOutputs(BaseModel):
    out: FilePath
    out_matrix: Optional[FilePath] = None
    out_message: str


class Reorient2stdNode(RHNode):
    input_spec = Reorient2stdInputs
    output_spec = Reorient2stdOutputs
    name = "reorient2std"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        outpath = job.directory / inputs.out_file if inputs.out_file is not None else job.directory / os.path.basename(inputs.in_file).replace('.nii.gz', '_r2s.nii.gz')
        
        cmd = ["fslreorient2std"]

        if inputs.output_matrix:
               outpath_xfm = job.directory / str(inputs.out_file).replace('.nii.gz', '.xfm') if inputs.out_file is not None else job.directory / os.path.basename(inputs.in_file).replace('.nii.gz', '_r2s.xfm')
               cmd += ['-m', outpath_xfm]
               
        
        # Add <input> <output>
        cmd += [str(inputs.in_file), str(outpath)]

        all_env_vars = os.environ.copy()
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)
    
        if inputs.output_matrix:
            return Reorient2stdOutputs(out=outpath, out_message=output, out_matrix=outpath_xfm)
        else:     
            return Reorient2stdOutputs(out=outpath, out_message=output)


app = Reorient2stdNode()