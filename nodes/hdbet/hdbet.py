from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import subprocess
import os

class HDBetInput(BaseModel):
    mr:FilePath
    out_file: Optional[str] = None

class HDBetOutput(BaseModel):
    masked_mr:FilePath
    mask:FilePath

class HDBetNode(RHNode):
    input_spec = HDBetInput
    output_spec = HDBetOutput
    name = "hdbet"
    required_gb_gpu_memory = 8
    required_num_threads = 2
    required_gb_memory = 8    

    def process(inputs, job):

        out_mri = job.directory / inputs.out_file if inputs.out_file is not None else job.directory / os.path.basename(inputs.mr).replace('.nii.gz', '_BET.nii.gz')
        out_mask= job.directory / (out_mri.name.replace('.nii.gz', '_mask.nii.gz'))

        cmd = ["hd-bet", "-i", str(inputs.mr), "-o", str(out_mri)]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        _ = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return HDBetOutput(masked_mr=out_mri, mask=out_mask)

app = HDBetNode()
