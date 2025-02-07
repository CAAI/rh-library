from rhnode import RHNode
from rhnode import RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import subprocess
import os

class DBougetInput(BaseModel):
    in_file:FilePath
    model_name:str = 'AGUNet'

class DBougetOutput(BaseModel):
    segmentation:FilePath

class DBougetNode(RHNode):
    input_spec = DBougetInput
    output_spec = DBougetOutput
    name = "dbouget"
    required_gb_gpu_memory = 6
    required_num_threads = 2
    required_gb_memory = 6

    def process(inputs,
                job):
        
        output = job.directory / "t1c-pred_Tumor.nii.gz"
        
        cli_cmd = ["python3.6",
                   "mri_brain_tumor_segmentation/main.py",
                   "-i", inputs.in_file,
                   "-o", str(output).replace('-pred_Tumor.nii.gz',''),
                   "-m", inputs.model_name,
                   "-g", str(job.device)]
        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        subprocess.check_output(cli_cmd, text=True,env=all_env_vars)
        
        return DBougetOutput(segmentation=output)

app = DBougetNode()