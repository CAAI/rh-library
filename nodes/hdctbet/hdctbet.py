from rhnode import RHNode
from pydantic import BaseModel, FilePath
import subprocess
import os

class HDCTBetInput(BaseModel):
    ct:FilePath

class HDCTBetOutput(BaseModel):
    masked_ct:FilePath
    mask:FilePath

class HDCTBetNode(RHNode):
    input_spec = HDCTBetInput
    output_spec = HDCTBetOutput
    name = "hdctbet"
    required_gb_gpu_memory = 8
    required_num_threads = 2
    required_gb_memory = 8    

    def process(inputs, job):

        out_ct = job.directory / "ct_masked.nii.gz"
        out_mask= job.directory / "ct_masked_mask.nii.gz"

        cmd = ["hd-ctbet", "-i", str(inputs.ct), "-o", str(out_ct)]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)

        return HDCTBetOutput(masked_ct=out_ct, mask=out_mask)

app = HDCTBetNode()
