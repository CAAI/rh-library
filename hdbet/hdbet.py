from rhnode import RHNode
from pydantic import BaseModel, FilePath
import subprocess
import os

class HDBetInput(BaseModel):
    mr:FilePath

class HDBetOutput(BaseModel):
    masked_mr:FilePath
    mask:FilePath

class HDBetNode(RHNode):
    input_spec = HDBetInput
    output_spec = HDBetOutput
    name = "hdbet"
    required_gb_gpu_memory = 8
    required_num_processes = 2
    required_gb_memory = 8    

    def process(inputs, job):

        out_mri = job.directory / "mri_masked.nii.gz"
        out_mask= job.directory / "mri_masked_mask.nii.gz"

        cmd = ["hd-bet", "-i", str(inputs.mr), "-o", str(out_mri)]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return HDBetOutput(masked_mr=out_mri, mask=out_mask)

app = HDBetNode()
