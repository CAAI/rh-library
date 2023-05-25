from rhnode import RHNode
from rhnode import NodeRunner
from pydantic import BaseModel, FilePath
import nibabel as nib
import subprocess

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
    required_gb_gpu_memory = 1
    required_num_processes = 1
    required_gb_memory = 1    
    
    def process(inputs,
                job):
        
        out_sbPET = job.directory / "sbPET.nii.gz"
        out_abn = job.directory / "abn.nii.gz"

        input_hd_bet = {"mr": inputs.mr}
        hdbet = NodeRunner("hdbet", input_hd_bet, job)
        hdbet.start()
        hdbet_output = hdbet.wait_for_finish()
        print("RUNNING zerodose CLI")
        cli_cmd = ["zerodose", 
                   "pipeline", "-i", str(inputs.mr), 
                   "-m", str(hdbet_output["mask"]) ,
                   "-p", str(inputs.pet),
                   "-oa", str(out_abn), 
                   "-os", str(out_sbPET),
                   "--no-img"]
        
        subprocess.check_output(cli_cmd, text=True)

        return ZeroDoseOutput(abn=out_abn, sb_pet=out_sbPET)


app = ZeroDoseNode()