from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess
import signal
import shutil
from pathlib import Path

class SynthmorphInputs(BaseModel):
    moving_file: FilePath
    command: str = 'register'
    fixed_file: FilePath = None # Required for 'register' command
    init_file: Optional[FilePath] = None # Required for 'apply' command
    xargs: Optional[str] = ''


class SynthmorphOutputs(BaseModel):
    moved_file: Optional[FilePath] = None
    trans_file: Optional[FilePath] = None
    out_message: str


class SynthmorphNode(RHNode):
    input_spec = SynthmorphInputs
    output_spec = SynthmorphOutputs
    name = "synthmorph"
    required_gb_gpu_memory = 15 # Probably higher!
    required_num_threads = 2
    required_gb_memory = 64

    @staticmethod
    def process(inputs, job):
        try:    
            out_moved = job.directory / "moved.nii.gz"
            
            
            if inputs.command == 'register':
                
                # Validate fixed_file is provided for register command
                if not inputs.fixed_file:
                    return SynthmorphOutputs(
                        out_message="Error: fixed_file is required for register command"
                    )
                
                if any(m in inputs.xargs for m in ['-m rigid', '-m affine']):
                    suffix = 'lta'
                else:
                    suffix = '.nii.gz'
                    
                out_trans = job.directory / f"trans.{suffix}"
                
                cmd = [
                    'mri_synthmorph',
                    'register',
                    '-g',
                    '-o', str(out_moved),
                    '-t', str(out_trans)
                ]
                
                if inputs.init_file is not None:
                    cmd += ['-i', str(inputs.init_file)]
            
                if inputs.xargs != '':
                    cmd += inputs.xargs.split()
                    
                cmd += [str(inputs.moving_file), str(inputs.fixed_file)]
                
                out_args = {
                    'moved_file': out_moved,
                    'trans_file': out_trans,
                    'out_message': ' '.join(cmd)
                }
                
            elif inputs.command == 'apply':
                
                if inputs.init_file is None:
                    return SynthmorphOutputs(
                        out_message="Error: init_file is required for apply command"
                    )
                                    
                cmd = [
                    'mri_synthmorph',
                    'apply',
                    str(inputs.init_file),
                    str(inputs.moving_file),
                    str(out_moved)
                ]
                
                if inputs.xargs != '':
                    cmd += inputs.xargs.split()
                    
                out_args = {
                    'moved_file': out_moved, 
                    'out_message': ' '.join(cmd)
                }
                
            else:
                return SynthmorphOutputs(
                    out_message=f"Error: Unknown command '{inputs.command}'. Supported commands: 'register', 'apply'"
                )
            
            all_env_vars = os.environ.copy()
            all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
            out = subprocess.check_output(cmd, text=True, env=all_env_vars)
            
            return SynthmorphOutputs(**out_args)
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output}"
            return SynthmorphOutputs(out_message=error_message)
        except Exception as e:
            error_message = f"Error during processing: {str(e)}"
            return SynthmorphOutputs(out_message=error_message)


app = SynthmorphNode()

"""

mri_synthmorph-register
synthmorph-1     | 
synthmorph-1     | NAME
synthmorph-1     |         mri_synthmorph-register - register 3D brain images without preprocessing
synthmorph-1     | 
synthmorph-1     | SYNOPSIS
synthmorph-1     |         mri_synthmorph register [options] moving fixed
synthmorph-1     | 
synthmorph-1     | DESCRIPTION
synthmorph-1     |         SynthMorph is a deep-learning tool for symmetric, acquisition-agnostic
synthmorph-1     |         registration of brain MRI with any volume size, resolution, and
synthmorph-1     |         orientation. The registration is anatomy-aware, removing the need for
synthmorph-1     |         skull-stripping, and you can control the warp smoothness.
synthmorph-1     | 
synthmorph-1     |         SynthMorph registers a moving (source) image to a fixed (target) image.
synthmorph-1     |         Their geometries can differ. The options are as follows:
synthmorph-1     | 
synthmorph-1     |         -m model
synthmorph-1     |                 Transformation model (joint, deform, affine, rigid). Defaults to
synthmorph-1     |                 joint. Joint includes affine and deformable but differs from
synthmorph-1     |                 running both in sequence in that it applies the deformable step
synthmorph-1     |                 in an affine mid-space to guarantee symmetric joint transforms.
synthmorph-1     |                 Deformable assumes prior affine alignment or initialization with
synthmorph-1     |                 -i.
synthmorph-1     | 
synthmorph-1     |         -o image
synthmorph-1     |                 Save moving registered to fixed.
synthmorph-1     | 
synthmorph-1     |         -O image
synthmorph-1     |                 Save fixed registered to moving.
synthmorph-1     | 
synthmorph-1     |         -H
synthmorph-1     |                 Update the voxel-to-world matrix instead of resampling when
synthmorph-1     |                 saving images with -o and -O. For matrix transforms only. Not
synthmorph-1     |                 all software supports headers with shear from affine
synthmorph-1     |                 registration.
synthmorph-1     | 
synthmorph-1     |         -t trans
synthmorph-1     |                 Save the transform from moving to fixed, including any
synthmorph-1     |                 initialization.
synthmorph-1     | 
synthmorph-1     |         -T trans
synthmorph-1     |                 Save the transform from fixed to moving, including any
synthmorph-1     |                 initialization.
synthmorph-1     | 
synthmorph-1     |         -i trans
synthmorph-1     |                 Apply an initial matrix transform to moving before the
synthmorph-1     |                 registration.
synthmorph-1     | 
synthmorph-1     |         -M
synthmorph-1     |                 Apply half the initial matrix transform to moving and (the
synthmorph-1     |                 inverse of) the other half to fixed, for symmetry. This will
synthmorph-1     |                 make running the deformable after an affine step equivalent to
synthmorph-1     |                 joint registration. Requires -i.
synthmorph-1     | 
synthmorph-1     |         -j threads
synthmorph-1     |                 Number of TensorFlow threads. System default if unspecified.
synthmorph-1     | 
synthmorph-1     |         -g
synthmorph-1     |                 Use the GPU in environment variable CUDA_VISIBLE_DEVICES or GPU
synthmorph-1     |                 0 if the variable is unset or empty.
synthmorph-1     | 
synthmorph-1     |         -r lambda
synthmorph-1     |                 Regularization parameter in the open interval (0, 1) for
synthmorph-1     |                 deformable registration. Higher values lead to smoother warps.
synthmorph-1     |                 Defaults to 0.5.
synthmorph-1     | 
synthmorph-1     |         -n steps
synthmorph-1     |                 Integration steps for deformable registration. Lower numbers
synthmorph-1     |                 improve speed and memory use but can lead to inaccuracies and
synthmorph-1     |                 folding voxels. Defaults to 7. Should not be less than 5.
synthmorph-1     | 
synthmorph-1     |         -e extent
synthmorph-1     |                 Isotropic extent of the registration space in unit voxels (192,
synthmorph-1     |                 256). Lower values improve speed and memory use but may crop the
synthmorph-1     |                 anatomy of interest. Defaults to 256.
synthmorph-1     | 
synthmorph-1     |         -w weights
synthmorph-1     |                 Use alternative model weights, exclusively. Repeat the flag to
synthmorph-1     |                 set affine and deformable weights for joint registration, or the
synthmorph-1     |                 result will disappoint.
synthmorph-1     | 
synthmorph-1     |         -h
synthmorph-1     |                 Print this help text and exit.
synthmorph-1     | 
synthmorph-1     | ENVIRONMENT
synthmorph-1     |         The following environment variables affect mri_synthmorph-register:
synthmorph-1     | 
synthmorph-1     |         CUDA_VISIBLE_DEVICES
synthmorph-1     |                 Use a specific GPU. If unset or empty, passing -g will select
synthmorph-1     |                 GPU 0. Ignored without -g.
synthmorph-1     | 
synthmorph-1     |         FREESURFER_HOME
synthmorph-1     |                 Load model weights from directory FREESURFER_HOME/models.
synthmorph-1     |                 Ignored when specifying weights with -w.
synthmorph-1     | 
synthmorph-1     | EXAMPLES
synthmorph-1     |         Joint affine-deformable registration, saving the moved image:
synthmorph-1     |                 # mri_synthmorph register -o out.nii mov.nii fix.nii
synthmorph-1     | 
synthmorph-1     |         Joint registration at 25% warp smoothness:
synthmorph-1     |                 # mri_synthmorph register -r 0.25 -o out.nii mov.nii fix.nii
synthmorph-1     | 
synthmorph-1     |         Affine registration saving the transform:
synthmorph-1     |                 # mri_synthmorph register -m affine -t aff.lta mov.nii.gz
synthmorph-1     |                 fix.nii.gz
synthmorph-1     | 
synthmorph-1     |         Deformable registration only, assuming prior affine alignment:
synthmorph-1     |                 # mri_synthmorph register -m deform -t def.mgz mov.mgz fix.mgz
synthmorph-1     | 
synthmorph-1     |         Deformable step initialized with an affine transform:
synthmorph-1     |                 # mri_synthmorph reg -m def -i aff.lta -o out.mgz mov.mgz
synthmorph-1     |                 fix.mgz
synthmorph-1     | 
synthmorph-1     |         Rigid registration, setting the output image header (no resampling):
synthmorph-1     |                 # mri_synthmorph register -m rigid -Ho out.mgz mov.mgz fix.mgz



"""