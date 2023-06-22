from rhnode import RHNode, RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import subprocess
import nibabel as nib
import numpy as np
import os
import shutil
from inference_pipeline.utils import get_template_fname

class BrainPETNRInputs(BaseModel):
    pet: FilePath
    scaling_factor: Optional[float] = 1.0
    ct: Optional[FilePath] = None
    out_filename: str
    model: Optional[str] = 'PiB'


class BrainPETNROutputs(BaseModel):
    denoised: FilePath
    pet_preprocessed: Optional[FilePath] = None
    pet_to_ct: Optional[FilePath] = None
    ct_preprocessed: Optional[FilePath] = None


class BrainPETNRNode(RHNode):
    input_spec = BrainPETNRInputs
    output_spec = BrainPETNROutputs
    name = "brainpetnr"

    required_gb_gpu_memory = 4
    required_num_threads = 4
    required_gb_memory = 8
    

    def process(inputs, job):

        out_args = {}

        # Scale PET input file
        scale_node = RHJob.from_parent_job("fslmaths", {
                'in_file': inputs.pet,  
                'xargs': '-mul %s' % str(inputs.scaling_factor),
                'out_file': 'PET_scaled.nii.gz'
            }, job, use_same_resources=True)
        scale_node.start()
        scale_output = scale_node.wait_for_finish()
        PET_scaled = scale_output['out']

        if inputs.ct is not None:

            # Perform skull strip
            hdctbet_node = RHJob.from_parent_job("hdctbet", {"ct": inputs.ct}, job, use_same_resources=True)
            hdctbet_node.start() # Dont wait for this to finish

            # Register PET to CT
            flirt_inputs = {"in_file": PET_scaled, 
                            "ref_file": inputs.ct,
                            "out_file": os.path.basename(inputs.pet).replace('.nii.gz', '_to_CT.nii.gz'),
                            "omat_file": os.path.basename(inputs.pet).replace('.nii.gz', '_to_CT.mat'),
                            "xargs": "-dof 6"}
            flirt_node = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_node.start() # Dont wait for this to finish

            # Wait for HD-CTBET here
            hdctbet_output = hdctbet_node.wait_for_finish()
            CT_BET = hdctbet_output['masked_ct']
            BETmask = hdctbet_output['mask']

            # Align CT_BET to avg
            flirt_inputs = {"in_file": CT_BET, 
                            "ref_file": get_template_fname(),
                            "out_file": os.path.basename(CT_BET).replace('.nii.gz', '_to_avg.nii.gz'),
                            "omat_file": os.path.basename(CT_BET).replace('.nii.gz', '_to_avg.mat'),
                            "xargs": "-dof 12"}
            flirt_node_avg = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_node_avg.start() 

            # Gather the two FLIRT processes
            flirt_output = flirt_node.wait_for_finish()
            PET_to_CT = flirt_output['out']
            PET_to_CT_OMAT = flirt_output['omat']
            out_args['pet_to_ct'] = PET_to_CT
            flirt_output_avg = flirt_node_avg.wait_for_finish()
            omat = flirt_output_avg['omat']

            # Concat XFM files
            concat_node = RHJob.from_parent_job("convertxfm", {
                    'in_file': PET_to_CT_OMAT, 
                    'second_file': omat, 
                    'concat': True,
                    'out_file': 'concat.xfm'
                }, job, use_same_resources=True)
            concat_node.start()
            concat_output = concat_node.wait_for_finish()
            concat_omat = concat_output['out']

            # Resample PET to avg
            flirt_inputs = {"in_file": PET_scaled, 
                            "ref_file": get_template_fname(),
                            "init_file": concat_omat,
                            "out_file": os.path.basename(inputs.pet).replace('.nii.gz', '_to_avg.nii.gz'),
                            "applyxfm": True}
            flirt_node_PET = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_node_PET.start()
            flirt_PET_output = flirt_node_PET.wait_for_finish()
            
            # Resample BETmask to avg
            flirt_inputs = {"in_file": BETmask, 
                            "ref_file": get_template_fname(),
                            "init_file": omat,
                            "out_file": 'BETmask_to_avg.nii.gz',
                            "applyxfm": True,
                            "xargs": "-interp nearestneighbour"}
            flirt_node_BET = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_node_BET.start()
            flirt_BET_output = flirt_node_BET.wait_for_finish()

            # Apply BETmask to PET in avg space
            img = nib.load(flirt_PET_output['out'])
            BET = nib.load(flirt_BET_output['out'])
            arr = img.get_fdata() * BET.get_fdata()
            img = nib.Nifti1Image(arr, img.affine, img.header)
            PET_preprocessed = job.directory / os.path.basename(inputs.pet).replace('.nii.gz', '_preprocessed.nii.gz')
            img.to_filename(PET_preprocessed)                

            # Done with preprocess. Output the files
            out_args['pet_preprocessed'] = PET_preprocessed
            out_args['ct_preprocessed'] = flirt_output_avg['out']
            PET = PET_preprocessed
        else:
            PET = PET_scaled

        # Call brainPETNR 
        denoised = job.directory / 'denoised_MNI_space.nii.gz' if inputs.ct is not None else job.directory / inputs.out_filename
        cmd = ['brainPETNR', '-pet', PET, '-o', str(denoised), '-model', inputs.model]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        _ = subprocess.check_output(cmd, text=True, env=all_env_vars)

        if inputs.ct is None:
            # No preprocessing was done, so nothing to invert
            return BrainPETNROutputs(denoised=denoised)
        else:
            # Invert preprocessing!

            # Invert XFM
            invert_node = RHJob.from_parent_job("convertxfm", {
                    'in_file': concat_omat,  
                    'inverse': True,
                    'out_file': 'inverted.xfm'
                }, job, use_same_resources=True)
            invert_node.start()
            invert_output = invert_node.wait_for_finish()
            invert_omat = invert_output['out']

            # Resample to patient space
            flirt_inputs = {"in_file": denoised, 
                            "ref_file": inputs.pet,
                            "init_file": invert_omat,
                            "out_file": 'denoised_patient_space.nii.gz',
                            "applyxfm": True}
            flirt_node_patient_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_node_patient_space.start()
            flirt_node_patient_space_output  = flirt_node_patient_space.wait_for_finish()      

            # Also resample BETmask
            flirt_inputs = {"in_file": flirt_BET_output['out'], 
                            "ref_file": inputs.pet,
                            "init_file": invert_omat,
                            "out_file": 'denoised_patient_space.nii.gz',
                            "applyxfm": True,
                            "xargs": "-interp nearestneighbour"}
            flirt_BET_node_patient_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
            flirt_BET_node_patient_space.start()
            flirt_BET_node_patient_space_output  = flirt_BET_node_patient_space.wait_for_finish()   

            # Blur lowdose
            blur_node = RHJob.from_parent_job("fslmaths", {
                    'in_file': PET_scaled,  
                    'xargs': '-s %s' % str(3.9 / 2.3548), # 2mm -> 5mm
                    'out_file': 'lowdose_smoothed.nii.gz'
                }, job, use_same_resources=True)
            blur_node.start()
            blur_output = blur_node.wait_for_finish()
            lowdose_blurred = blur_output['out']

            # Merge lowdose and denoised PET
            img_denoised = nib.load(flirt_node_patient_space_output['out'])
            BET = nib.load(flirt_BET_node_patient_space_output['out']).get_fdata()
            arr = nib.load(lowdose_blurred).get_fdata()
            arr[BET>0] = img_denoised.get_fdata()[BET>0]
            img = nib.Nifti1Image(arr, img_denoised.affine, img_denoised.header)
            out_args['denoised'] = job.directory / inputs.out_filename
            img.to_filename(out_args['denoised'])

        return BrainPETNROutputs(**out_args)


app = BrainPETNRNode()