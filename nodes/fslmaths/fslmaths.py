from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import subprocess


class FSLMathsInputs(BaseModel):
    in_file: FilePath
    xargs: Optional[str] = None
    second_file: Optional[FilePath] = None
    out_file: str


class FSLMathsOutputs(BaseModel):
    out: FilePath
    out_message: str


class FSLMathsNode(RHNode):
    input_spec = FSLMathsInputs
    output_spec = FSLMathsOutputs
    name = "fslmaths"
    required_gb_gpu_memory = 0
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        outpath = job.directory / inputs.out_file
        
        cmd = ["fslmaths",
               str(inputs.in_file)]
        cmd += inputs.xargs.split(' ')
        if inputs.second_file is not None:
            cmd += inputs.second_file
        cmd += [str(outpath)]

        all_env_vars = os.environ.copy()
        output = subprocess.check_output(cmd, text=True,env=all_env_vars)
    
        return FSLMathsOutputs(out=outpath, out_message=output)


app = FSLMathsNode()

"""

Usage: fslmaths [-dt <datatype>] <first_input> [operations and inputs] <output> [-odt <datatype>]

Datatype information:
 -dt sets the datatype used internally for calculations (default float for all except double images)
 -odt sets the output datatype ( default is float )
 Possible datatypes are: char short int float double input
 "input" will set the datatype to that of the original image

Binary operations:
  (some inputs can be either an image or a number)
 -add   : add following input to current image
 -sub   : subtract following input from current image
 -mul   : multiply current image by following input
 -div   : divide current image by following input
 -rem   : modulus remainder - divide current image by following input and take remainder
 -mas   : use (following image>0) to mask current image
 -thr   : use following number to threshold current image (zero anything below the number)
 -thrp  : use following percentage (0-100) of ROBUST RANGE to threshold current image (zero anything below the number)
 -thrP  : use following percentage (0-100) of ROBUST RANGE of non-zero voxels and threshold below
 -uthr  : use following number to upper-threshold current image (zero anything above the number)
 -uthrp : use following percentage (0-100) of ROBUST RANGE to upper-threshold current image (zero anything above the number)
 -uthrP : use following percentage (0-100) of ROBUST RANGE of non-zero voxels and threshold above
 -max   : take maximum of following input and current image
 -min   : take minimum of following input and current image
 -seed  : seed random number generator with following number
 -restart : replace the current image with input for future processing operations
 -save : save the current working image to the input filename

Basic unary operations:
 -exp   : exponential
 -log   : natural logarithm
 -sin   : sine function
 -cos   : cosine function
 -tan   : tangent function
 -asin  : arc sine function
 -acos  : arc cosine function
 -atan  : arc tangent function
 -sqr   : square
 -sqrt  : square root
 -recip : reciprocal (1/current image)
 -abs   : absolute value
 -bin   : use (current image>0) to binarise
 -binv  : binarise and invert (binarisation and logical inversion)
 -fillh : fill holes in a binary mask (holes are internal - i.e. do not touch the edge of the FOV)
 -fillh26 : fill holes using 26 connectivity
 -index : replace each nonzero voxel with a unique (subject to wrapping) index number
 -grid <value> <spacing> : add a 3D grid of intensity <value> with grid spacing <spacing>
 -edge  : edge strength
 -tfce <H> <E> <connectivity>: enhance with TFCE, e.g. -tfce 2 0.5 6 (maybe change 6 to 26 for skeletons)
 -tfceS <H> <E> <connectivity> <X> <Y> <Z> <tfce_thresh>: show support area for voxel (X,Y,Z)
 -nan   : replace NaNs (improper numbers) with 0
 -nanm  : make NaN (improper number) mask with 1 for NaN voxels, 0 otherwise
 -rand  : add uniform noise (range 0:1)
 -randn : add Gaussian noise (mean=0 sigma=1)
 -inm <mean> :  (-i i ip.c) intensity normalisation (per 3D volume mean)
 -ing <mean> :  (-I i ip.c) intensity normalisation, global 4D mean)
 -range : set the output calmin/max to full data range

Matrix operations:
 -tensor_decomp : convert a 4D (6-timepoint )tensor image into L1,2,3,FA,MD,MO,V1,2,3 (remaining image in pipeline is FA)

Kernel operations (set BEFORE filtering operation if desired):
 -kernel 3D : 3x3x3 box centered on target voxel (set as default kernel)
 -kernel 2D : 3x3x1 box centered on target voxel
 -kernel box    <size>     : all voxels in a cube of width <size> mm centered on target voxel
 -kernel boxv   <size>     : all voxels in a cube of width <size> voxels centered on target voxel, CAUTION: size should be an odd number
 -kernel boxv3  <X> <Y> <Z>: all voxels in a cuboid of dimensions X x Y x Z centered on target voxel, CAUTION: size should be an odd number
 -kernel gauss  <sigma>    : gaussian kernel (sigma in mm, not voxels)
 -kernel sphere <size>     : all voxels in a sphere of radius <size> mm centered on target voxel
 -kernel file   <filename> : use external file as kernel

Spatial Filtering operations: N.B. all options apart from -s use the default kernel or that _previously_ specified by -kernel
 -dilM    : Mean Dilation of non-zero voxels
 -dilD    : Modal Dilation of non-zero voxels
 -dilF    : Maximum filtering of all voxels
 -dilall  : Apply -dilM repeatedly until the entire FOV is covered
 -ero     : Erode by zeroing non-zero voxels when zero voxels found in kernel
 -eroF    : Minimum filtering of all voxels
 -fmedian : Median Filtering
 -fmean   : Mean filtering, kernel weighted (conventionally used with gauss kernel)
 -fmeanu  : Mean filtering, kernel weighted, un-normalised (gives edge effects)
 -s <sigma> : create a gauss kernel of sigma mm and perform mean filtering
 -subsamp2  : downsamples image by a factor of 2 (keeping new voxels centred on old)
 -subsamp2offc  : downsamples image by a factor of 2 (non-centred)

Dimensionality reduction operations:
  (the "T" can be replaced by X, Y or Z to collapse across a different dimension)
 -Tmean   : mean across time
 -Tstd    : standard deviation across time
 -Tmax    : max across time
 -Tmaxn   : time index of max across time
 -Tmin    : min across time
 -Tmedian : median across time
 -Tperc <percentage> : nth percentile (0-100) of FULL RANGE across time
 -Tar1    : temporal AR(1) coefficient (use -odt float and probably demean first)

Basic statistical operations:
 -pval    : Nonparametric uncorrected P-value, assuming timepoints are the permutations; first timepoint is actual (unpermuted) stats image
 -pval0   : Same as -pval, but treat zeros as missing data
 -cpval   : Same as -pval, but gives FWE corrected P-values
 -ztop    : Convert Z-stat to (uncorrected) P
 -ptoz    : Convert (uncorrected) P to Z
 -rank    : Convert data to ranks (over T dim)
 -ranknorm: Transform to Normal dist via ranks

Multi-argument operations:
 -roi <xmin> <xsize> <ymin> <ysize> <zmin> <zsize> <tmin> <tsize> : zero outside roi (using voxel coordinates). Inputting -1 for a size will set it to the full image extent for that dimension.
 -bptf  <hp_sigma> <lp_sigma> : (-t in ip.c) Bandpass temporal filtering; nonlinear highpass and Gaussian linear lowpass (with sigmas in volumes, not seconds); set either sigma<0 to skip that filter
 -roc <AROC-thresh> <outfile> [4Dnoiseonly] <truth> : take (normally binary) truth and test current image in ROC analysis against truth. <AROC-thresh> is usually 0.05 and is limit of Area-under-ROC measure FP axis. <outfile> is a text file of the ROC curve (triplets of values: FP TP threshold). If the truth image contains negative voxels these get excluded from all calculations. If <AROC-thresh> is positive then the [4Dnoiseonly] option needs to be set, and the FP rate is determined from this noise-only data, and is set to be the fraction of timepoints where any FP (anywhere) is seen, as found in the noise-only 4d-dataset. This is then controlling the FWE rate. If <AROC-thresh> is negative the FP rate is calculated from the zero-value parts of the <truth> image, this time averaging voxelwise FP rate over all timepoints. In both cases the TP rate is the average fraction of truth=positive voxels correctly found.

Combining 4D and 3D images:
 If you apply a Binary operation (one that takes the current image and a new image together), when one is 3D and the other is 4D,
 the 3D image is cloned temporally to match the temporal dimensions of the 4D image.

e.g. fslmaths inputVolume -add inputVolume2 output_volume
     fslmaths inputVolume -add 2.5 output_volume
     fslmaths inputVolume -add 2.5 -mul inputVolume2 output_volume

     fslmaths 4D_inputVolume -Tmean -mul -1 -add 4D_inputVolume demeaned_4D_inputVolume

     
"""