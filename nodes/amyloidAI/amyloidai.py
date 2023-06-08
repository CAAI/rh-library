from rhnode import RHNode, RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess
from amyloidAI.run import run
from amyloidAI.utils import get_MRI_template_fname, get_CT_template_fname
import nibabel as nib


class AmyloidAIInputs(BaseModel):
    PET_file: FilePath
    MRI_file: Optional[FilePath] = None
    CT_file: Optional[FilePath] = None


class AmyloidAIOutputs(BaseModel):
    suvr: float
    suvr_std: float
    diagnosis: float
    diagnosis_std: float


class AmyloidAINode(RHNode):
    input_spec = AmyloidAIInputs
    output_spec = AmyloidAIOutputs
    name = "amyloidai"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        PET_file = inputs.PET_file

        # Check if anatomical file is set
        if inputs.MRI_file is not None and inputs.CT_file is not None:
            raise ValueError('Cannot use both CT_file and MRI_file')
        elif inputs.MRI_file is not None or inputs.CT_file is not None:

            # Set values specific for MR or CT based BET and spatial normalization
            masked_file_key = 'masked_mr' if inputs.MRI_file is not None else 'masked_ct'
            target_template = get_MRI_template_fname if inputs.MRI_file is not None else get_CT_template_fname
            node_name = 'hdbet' if inputs.MRI_file is not None else 'hdctbet'
            node_key = 'mr' if inputs.MRI_file is not None else 'ct'
            node_input = inputs.MRI_file if inputs.MRI_file is not None else inputs.CT_file

            # Perform BET (HD_BET or HD_CTBET)
            hd_bet_node = RHJob.from_parent_job(node_name, {node_key: node_input}, job)
            hd_bet_node.start()
            hd_bet_output = hd_bet_node.wait_for_finish()

            # Register to MNI
            affine = job.directory / "aff.txt"
            cmd = ['reg_aladin', 
                   '-ref', target_template(), 
                   '-flo', hd_bet_output[masked_file_key],
                   '-aff', affine]
            output = subprocess.check_output(cmd, text=True)

            # Resample BET mask to MNI
            BET_file = job.directory / 'mask_affine.nii.gz'
            cmd = ['reg_resample',
                   '-ref', get_CT_template_fname(),
                   '-flo', hd_bet_output['mask'],
                   '-trans', affine,
                   '-inter', 'NN',
                   '-res', BET_file]
            output = subprocess.check_output(cmd, text=True)

            # Resample PET to MNI
            PET_affine = job.directory / 'PET_affine.nii.gz'
            cmd = ['reg_resample',
                   '-ref', get_CT_template_fname(),
                   '-flo', PET_file,
                   '-trans', affine,
                   '-inter', 'LIN',
                   '-res', PET_affine]
            output = subprocess.check_output(cmd, text=True)

            # Apply BET mask to PET in MNI space
            img = nib.load(PET_affine)
            BET = nib.load(BET_file)
            arr = img.get_fdata() * BET.multiplier
            img = nib.Nifti1Image(arr, img.affine, img.header)
            PET_file = job.directory / "PET_affine_BET.nii.gz"
            img.to_filename(PET_file)

        output = run(PET_file)
        
    
        return AmyloidAIOutputs(**output)


app = AmyloidAINode()
