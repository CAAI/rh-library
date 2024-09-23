from rhnode import RHNode
from pydantic import BaseModel, FilePath, DirectoryPath
from typing import Optional
import subprocess
import os

class SynthSegInput(BaseModel):
    in_file:FilePath
    parc: Optional[bool]=False
    robust: Optional[bool]=False
    ct: Optional[bool]=False
    # vol: Optional[str]=""
    # qc: Optional[str]=""
    # resample: Optional[str]=""


class SynthSegOutput(BaseModel):
    out_segmentation:FilePath
    # out_vol:Optional[FilePath]
    # out_qc:Optional[FilePath]
    # out_resample:Optional[FilePath]
    

class SynthSegNode(RHNode):
    input_spec = SynthSegInput
    output_spec = SynthSegOutput
    name = "synthseg"
    required_gb_gpu_memory = 12
    required_num_threads = 2
    required_gb_memory = 12    

    def process(inputs, job):
        out_file = job.directory / 'segmentation.nii.gz'
        
        # Optional files
        vol_file = None
        qc_file = None
        resample_file = None

        cmd = ["python", "/app/SynthSeg/scripts/commands/SynthSeg_predict.py", "--i", str(inputs.in_file), "--o", str(out_file)]
        
        cmd_args = []
        if inputs.parc:
            cmd_args += ['--parc']
        if inputs.robust:
            cmd_args += ['--robust']
        if inputs.ct:
            cmd_args += ['--ct']
        """
        if inputs.vol != "":
            vol_file = job.directory / (inputs.vol+'.csv') if not str(inputs.vol).endswith('.csv') else job.directory / inputs.vol
            cmd_args += ['--vol'] + [vol_file]
        if inputs.qc != "":
            qc_file = job.directory / (inputs.qc+'.csv') if not str(inputs.qc).endswith('.csv') else job.directory / inputs.qc
            cmd_args += ['--qc'] + [qc_file]
        if inputs.resample != "":
            resample_file = job.directory / (inputs.resample+'.nii.gz') if not str(inputs.resample).endswith('.nii.gz') else job.directory / inputs.resample
            cmd_args += ['--resample'] + [resample_file]
        """
         
        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        out = subprocess.check_output(cmd+cmd_args, text=True,env=all_env_vars)
        
        return SynthSegOutput(out_segmentation=out_file)
        
        """
        out_args = {'out_segmentation': out_file}
        if vol_file is not None:
            out_args['out_vol'] = vol_file
        if qc_file is not None:
            out_args['out_qc'] = qc_file
        if resample_file is not None:
            out_args['out_resample'] = resample_file
        return SynthSegOutput(**out_args)
        """

app = SynthSegNode()
