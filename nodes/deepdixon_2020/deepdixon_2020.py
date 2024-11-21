from rhnode import RHNode
from rhnode import RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import nibabel as nib
import subprocess
import os
import numpy as np
import shutil
from numpy.lib import stride_tricks
import tensorflow as tf

class DeepDixonInput(BaseModel):
    in_phase:FilePath
    out_phase:FilePath
    mMR_version:str = 'E11'

class DeepDixonOutput(BaseModel):
    deepdixon:FilePath
    
"""
Helper function to cut patches out of data
"""
def cutup(data, blck, strd):
    sh = np.array(data.shape)
    blck = np.asanyarray(blck)
    strd = np.asanyarray(strd)
    nbl = (sh - blck) // strd + 1
    strides = np.r_[data.strides * strd, data.strides]
    dims = np.r_[nbl, blck]
    data6 = stride_tricks.as_strided(data, strides=strides, shape=dims)
    return data6
    
def resample_images(dataset1_nib,dataset2_nib,version):
    
    dataset1 = dataset1_nib.get_fdata()
    dataset2 = dataset2_nib.get_fdata()
    
    if version == 'E11':
        sub1 = dataset1[96:288,6:198,:]
        sub2 = dataset2[96:288,6:198,:]
        swap1 = np.swapaxes(sub1,0,2)
        swap2 = np.swapaxes(sub2,0,2)
        
        flip1 = np.flipud(swap1)
        flip2 = np.flipud(swap2)
        
        flip1 = np.fliplr(flip1)
        flip2 = np.fliplr(flip2)
        
        flip1 = np.flip(flip1, 2).astype(np.float32)
        flip2 = np.flip(flip2, 2).astype(np.float32)
        
    elif version == 'B20P':
        sub1 = dataset1[64:256,32:224,:]
        sub2 = dataset2[64:256,32:224,:]
    
        swap1 = np.swapaxes(sub1,0,2)
        swap2 = np.swapaxes(sub2,0,2)
        flip1 = np.fliplr(swap1)
        flip2 = np.fliplr(swap2)
    
    return flip1,flip2

"""
Return all combinations of 192x192x16 patches from each image with stride 2
"""
def get_patches_znorm(vol1,vol2=None,normalize_both=True):
    mean_vol1, std_vol1 = ( np.mean(vol1[np.where(vol1>0)]), np.std(vol1[np.where(vol1>0)]) )
    
    mean_vol2, std_vol2 = ( np.mean(vol2[np.where(vol2>0)]), np.std(vol2[np.where(vol2>0)]) )
    
    # STANDARDIZE
    vol1 = np.true_divide( vol1 - mean_vol1, std_vol1 ) if normalize_both else np.true_divide( vol1 - mean_vol2, std_vol2 )
    vol2 = np.true_divide( vol2 - mean_vol2, std_vol2 )
        
    patches_vol1 = cutup(vol1,(16,192,192),(2,1,1))
    patches_vol2 = cutup(vol2,(16,192,192),(2,1,1))

    ijk = patches_vol1.shape[0]*patches_vol1.shape[1]*patches_vol1.shape[2]
    
    selected_patches = np.empty((ijk,16,192,192,2), dtype='float32')
    selected_patches[:,:,:,:,0] = np.reshape(patches_vol1,(ijk,16,192,192))
    selected_patches[:,:,:,:,1] = np.reshape(patches_vol2,(ijk,16,192,192))
    
    return selected_patches

"""
Predicts patches of pCT data from patches of UTE data, 
and combines the result by averaging overlapping patches
"""
def predict(model,patches,out_shape):
    
    # Settings for patch extraction
    h = 16 # Number of slices 
    sh = 2 # Patch stride

    # Container matrices for data and counter for overlapping patches
    predicted_combined = np.zeros(out_shape)
    predicted_counter = np.zeros(out_shape)

    # Process a patch at a time
    for p in range(patches.shape[0]):
        from_h = p*sh # Start slice of patch
        predicted = model.predict(np.reshape(patches[p,:,:,:,:],(1,16,192,192,patches.shape[-1]))) # Predict pCT for patch
        predicted[ predicted == np.nan ] = -1 # Can occur, remove so output does not fail, but set to a value that can be searched for
        predicted_combined[from_h:from_h+h,:,:] += np.reshape(predicted,(16,192,192)) # Insert into container
        predicted_counter[from_h:from_h+h,:,:] += 1 # Update counter in area of patch for later average

    predicted_combined = np.divide(predicted_combined,predicted_counter) # Average over overlapping patches
    predicted_combined[ predicted_combined == np.inf ] = 0 # If divide by zero, remove here (should not occur since counter >> 0).
    
    return predicted_combined

class DeepDixonNode(RHNode):
    input_spec = DeepDixonInput
    output_spec = DeepDixonOutput
    name = "deepdixon_2020"
    required_gb_gpu_memory = 6
    required_num_threads = 2
    required_gb_memory = 12

    def process(inputs,
                job):
        
        if inputs.mMR_version == 'E11':
            isoxfm = 1.3021
            model_name = 'DeepDixon_VE11P_model1_TF2.h5'
        elif inputs.mMR_version == 'B20P':
            isoxfm = 1.5626
            model_name = 'DeepDixon_VB20P_TF2.h5'
        else:
            raise ValueError('Software version not implemented: ', inputs.mMR_version)

        input_flirt = {'xargs': f'-applyisoxfm {isoxfm}'}

        rsl = {}
        for mr_name, mr in zip(['in_phase','out_phase'],[inputs.in_phase, inputs.out_phase]):
            
            # BUG https://github.com/CAAI/rh-node/issues/26
            # FIX THE FACT THAT REF_FILE AND FILE CAN BE THE SAME,
            # WHICH IS NOT ALLOWED IN RHNode
            ref_file = job.directory / os.path.basename(mr).replace('.nii.gz', '_ref.nii.gz')
            shutil.copyfile(mr, ref_file)
            
            input_flirt['in_file'] = mr
            input_flirt['ref_file'] = ref_file
            input_flirt['out_file'] = f'{mr_name}.nii.gz'
            flirt = RHJob.from_parent_job("flirt", input_flirt, job, use_same_resources=True)
            flirt.start()
            flirt_output = flirt.wait_for_finish()
            rsl[mr_name] = flirt_output["out"]

        # Load and resample
        out_phase = nib.load(rsl['out_phase'])
        in_phase = nib.load(rsl['in_phase'])
        out_phase_rsl,in_phase_rsl = resample_images(out_phase, in_phase, version=inputs.mMR_version)

        # Load all patches
        patches = get_patches_znorm(in_phase_rsl,out_phase_rsl, normalize_both=True)
        
        # Predict
        model = tf.keras.models.load_model(f'/models/DeepDixon/{model_name}',compile=False)
        DeepX = predict(model, patches, out_shape=in_phase_rsl.shape)

        # Rehape to in-phase resolution
        DeepX_padded = np.zeros(out_phase.shape)
        if inputs.mMR_version == 'E11':
            DeepX = np.swapaxes(np.flipud(np.fliplr(np.flip(DeepX,2))),2,0)
            DeepX_padded[96:288,6:198,:] = DeepX
        elif inputs.mMR_version == 'B20P':
            DeepX = np.swapaxes(np.fliplr(DeepX),2,0)
            DeepX_padded[64:256,32:224,:] = DeepX
        DeepX_nii = nib.Nifti1Image(DeepX_padded,out_phase.affine, out_phase.header)
        out_deepdixon = job.directory / "DeepDixon.nii.gz"
        nib.save(DeepX_nii, out_deepdixon)
        
        return DeepDixonOutput(deepdixon=out_deepdixon)

app = DeepDixonNode()