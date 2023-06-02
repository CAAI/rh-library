from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess


class FLIRTInputs(BaseModel):
    in_file: FilePath
    ref_file: FilePath
    out_file: str = None
    omat_file: str = None
    applyxfm: Optional[bool] = False
    init_file: Optional[FilePath] = None
    xargs: Optional[str] = ''


class FLIRTOutputs(BaseModel):
    out: Optional[FilePath] = None
    omat: Optional[FilePath] = None
    out_message: str


class FLIRTNode(RHNode):
    input_spec = FLIRTInputs
    output_spec = FLIRTOutputs
    name = "flirt"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        outargs = {}

        # Add optional output files
        if inputs.out_file is not None:
            outargs['out'] = str(job.directory / inputs.out_file)
        if inputs.omat_file is not None:
            outargs['omat'] = str(job.directory / inputs.omat_file)
        
        cmd = ["flirt",
               "-in", str(inputs.in_file),
               "-ref", str(inputs.ref_file)]

        # Check if function called with registration or resampling option
        if inputs.applyxfm:
            assert inputs.out_file is not None, "out_file cannot be none when using applyxfm flag"
            assert inputs.init_file is not None, "init_file cannot be none when using applyxfm flag"
            cmd = cmd + ['-applyxfm', '-init', str(inputs.init_file), '-out', outargs['out']]
        else:
            if inputs.omat_file is not None:
                cmd = cmd + ['-omat', outargs['omat']]
            if inputs.out_file is not None:
                cmd = cmd + ['-out', outargs['out']]
            
        # Add custom xargs (see comment block below for arguments)
        cmd = cmd + inputs.xargs.split(' ')

        all_env_vars = os.environ.copy()
        outargs['out_message'] = subprocess.check_output(cmd, text=True,env=all_env_vars)
    
        return FLIRTOutputs(**outargs)


app = FLIRTNode()

"""

Usage: flirt [options] -in <inputvol> -ref <refvol> -out <outputvol>
       flirt [options] -in <inputvol> -ref <refvol> -omat <outputmatrix>
       flirt [options] -in <inputvol> -ref <refvol> -applyxfm -init <matrix> -out <outputvol>

  Available options are:
        -in  <inputvol>                    (no default)
        -ref <refvol>                      (no default)
        -init <matrix-filname>             (input 4x4 affine matrix)
        -omat <matrix-filename>            (output in 4x4 ascii format)
        -out, -o <outputvol>               (default is none)
        -datatype {char,short,int,float,double}                    (force output data type)
        -cost {mutualinfo,corratio,normcorr,normmi,leastsq,labeldiff,bbr}        (default is corratio)
        -searchcost {mutualinfo,corratio,normcorr,normmi,leastsq,labeldiff,bbr}  (default is corratio)
        -usesqform                         (initialise using appropriate sform or qform)
        -displayinit                       (display initial matrix)
        -anglerep {quaternion,euler}       (default is euler)
        -interp {trilinear,nearestneighbour,sinc,spline}  (final interpolation: def - trilinear)
        -sincwidth <full-width in voxels>  (default is 7)
        -sincwindow {rectangular,hanning,blackman}
        -bins <number of histogram bins>   (default is 256)
        -dof  <number of transform dofs>   (default is 12)
        -noresample                        (do not change input sampling)
        -forcescaling                      (force rescaling even for low-res images)
        -minsampling <vox_dim>             (set minimum voxel dimension for sampling (in mm))
        -applyxfm                          (applies transform (no optimisation) - requires -init)
        -applyisoxfm <scale>               (as applyxfm but forces isotropic resampling)
        -paddingsize <number of voxels>    (for applyxfm: interpolates outside image by size)
        -searchrx <min_angle> <max_angle>  (angles in degrees: default is -90 90)
        -searchry <min_angle> <max_angle>  (angles in degrees: default is -90 90)
        -searchrz <min_angle> <max_angle>  (angles in degrees: default is -90 90)
        -nosearch                          (sets all angular search ranges to 0 0)
        -coarsesearch <delta_angle>        (angle in degrees: default is 60)
        -finesearch <delta_angle>          (angle in degrees: default is 18)
        -schedule <schedule-file>          (replaces default schedule)
        -refweight <volume>                (use weights for reference volume)
        -inweight <volume>                 (use weights for input volume)
        -wmseg <volume>                    (white matter segmentation volume needed by BBR cost function)
        -wmcoords <text matrix>            (white matter boundary coordinates for BBR cost function)
        -wmnorms <text matrix>             (white matter boundary normals for BBR cost function)
        -fieldmap <volume>                 (fieldmap image in rads/s - must be already registered to the reference image)
        -fieldmapmask <volume>             (mask for fieldmap image)
        -pedir <index>                     (phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z)
        -echospacing <value>               (value of EPI echo spacing - units of seconds)
        -bbrtype <value>                   (type of bbr cost function: signed [default], global_abs, local_abs)
        -bbrslope <value>                  (value of bbr slope)
        -setbackground <value>             (use specified background value for points outside FOV)
        -noclamp                           (do not use intensity clamping)
        -noresampblur                      (do not use blurring on downsampling)
        -2D                                (use 2D rigid body mode - ignores dof)
        -verbose <num>                     (0 is least and default)
        -v                                 (same as -verbose 1)
        -i                                 (pauses at each stage: default is off)
        -version                           (prints version number)
        -help


"""