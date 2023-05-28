from rhnode import RHNode
from rhnode import RHJob
from pydantic import BaseModel, FilePath
import nibabel as nib
import subprocess
import os 

class ZeroDoseInput(BaseModel):
    pet:FilePath
    mr:FilePath
    mask: FilePath = None
    do_registration: bool = True

class ZeroDoseOutput(BaseModel):
    abn:FilePath
    sb_pet:FilePath


class ZeroDoseNode(RHNode):
    input_spec = ZeroDoseInput
    output_spec = ZeroDoseOutput
    name = "zerodose"
    required_gb_gpu_memory = 8
    required_num_threads = 2
    required_gb_memory = 8    

    def process(inputs,
                job):
    
        out_sbPET = job.directory / "sbPET.nii.gz"
        out_abn = job.directory / "abn.nii.gz"

        input_hd_bet = {"mr": inputs.mr}

        hdbet = RHJob.from_parent_job("hdbet", input_hd_bet, job, use_same_resources=True)
        hdbet.start()
        hdbet_output = hdbet.wait_for_finish()

        cli_cmd = ["zerodose", 
                   "pipeline", "-i", str(inputs.mr), 
                   "-m", str(hdbet_output["mask"]) ,
                   "-p", str(inputs.pet),
                   "-oa", str(out_abn), 
                   "-os", str(out_sbPET),
                   "--no-img"]
        
        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        subprocess.check_output(cli_cmd, text=True,env=all_env_vars)
        
        return ZeroDoseOutput(abn=out_abn, sb_pet=out_sbPET)

app = ZeroDoseNode()