from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess
import signal
import shutil
from pathlib import Path

class SynthmorphInputs(BaseModel):
    moving_file: FilePath
    fixed_file: FilePath = None
    init_file: Optional[FilePath] = None
    xargs: Optional[str] = ''


class SynthmorphOutputs(BaseModel):
    moved_file: Optional[FilePath] = None
    trans_file: Optional[FilePath] = None
    out_message: str


class SynthmorphNode(RHNode):
    input_spec = SynthmorphInputs
    output_spec = SynthmorphOutputs
    name = "synthmorph"
    required_gb_gpu_memory = 4 # Probably higher!
    required_num_threads = 1
    required_gb_memory = 8 

    def process(inputs, job):
            
        out_trans = job.directory / "trans.nii.gz"
        out_moved = job.directory / "moved.nii.gz"
        
        cmd = [
                'mri_synthmorph',
                '-g',
                '-o', str(out_moved),
                '-t', str(out_trans)
        ]
        
        if inputs.init_file is not None:
                cmd += ['-i', str(inputs.init_file)]
        
        if inputs.xargs != '':
                cmd += inputs.xargs.split( )
                
        cmd += [str(inputs.moving_file), str(inputs.fixed_file)]
        
        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        out = subprocess.check_output(cmd, text=True, env=all_env_vars)
        
        output = ' '.join(cmd)
        
        return SynthmorphOutputs(moved_file=out_moved, trans_file=out_trans, out_message=output)


app = SynthmorphNode()
