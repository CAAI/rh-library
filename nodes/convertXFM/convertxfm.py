from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess


class ConvertXFMInputs(BaseModel):
    in_file: FilePath
    second_file: Optional[FilePath] = None
    concat: Optional[bool] = False
    fixscaleskew: Optional[bool] = False
    inverse: Optional[bool] = False
    out_file: str


class ConvertXFMOutputs(BaseModel):
    out: FilePath
    out_message: str


class ConvertXFMNode(RHNode):
    input_spec = ConvertXFMInputs
    output_spec = ConvertXFMOutputs
    name = "convertxfm"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        outpath = job.directory / inputs.out_file
        
        cmd = ["convert_xfm",
               '-omat',
               str(outpath)]
        
        if inputs.concat:
            cmd += ['-concat', str(inputs.second_file)]
        elif inputs.fixscaleskew:
            cmd += ['-fixscaleskew', str(inputs.second_file)]
        
        if inputs.inverse:
            cmd += ['-inverse']

        # Add input file
        cmd += [str(inputs.in_file)]
        """
        Usage: convert_xfm [options] <input-matrix-filename>
        e.g. convert_xfm -omat <outmat> -inverse <inmat>
            convert_xfm -omat <outmat_AtoC> -concat <mat_BtoC> <mat_AtoB>

        Available options are:
                -omat <matrix-filename>            (4x4 ascii format)
                -concat <second-matrix-filename>
                -fixscaleskew <second-matrix-filename>
                -inverse                           (Reference image must be the one originally used)

        """

        all_env_vars = os.environ.copy()
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)
    
        return ConvertXFMOutputs(out=outpath, out_message=output)


app = ConvertXFMNode()