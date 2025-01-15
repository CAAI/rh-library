# rh-library
A collection of deployment ready machine learning tools developed by CAAI. Each model is packaged in rh-node to enable easy deployment with docker.

## CAAI nodes
Tools developed by members of CAAI, packaged in rh-node. 
| **node** |**dicom**| **description** | **dependencies** | **project** |
|---|---|---|---|---|
| [zerodose](nodes/zerodose) |[link](dicom_nodes/zerodose) |FDG anomaly detection| hdbet | https://github.com/CAAI/zerodose |
| [hdctbet](nodes/hdctbet) | | CT brain extraction|  | https://github.com/CAAI/HD-CTBET |
| [amyloidai](nodes/amyloidAI) | | Amyloid status estimation | hdbet, hdctbet | https://github.com/CAAI/amyloidAI |
| [aims](nodes/aims) | | MS lesions segmentation | hdbet, flirt, reorient2std | https://github.com/CAAI/AIMS |
| [brainpetnr](nodes/brainPETNR) | | PET denoising for PE2I and PiB| hdctbet, flirt, fslmaths, convertXFM | https://github.com/CAAI/brainPETNR |
| [pe2idenoiser](nodes/pe2idenoiser) | | PET denoising for Vision and Quadra PE2I | hdctbet, flirt, fslmaths, convertXFM | https://github.com/CAAI/PE2I_denoiser |
| [public_glio](nodes/public_glio) | | Glioma segmentation from MRI | hdbet, flirt, reorient2std, convertXFM | https://github.com/DEPICT-RH/public_glio |

## General purpose nodes
Other tools, packaged in rh-node. 
| **node** | **description** | **dependencies** | **project** |
|---|---|---|---|
| [hdbet](nodes/hdbet) | MRI brain extraction |  | https://github.com/MIC-DKFZ/HD-BET |
| [synthseg](nodes/synthseg) | MRI brain segmentation |  | https://github.com/BBillot/SynthSeg |
| [reorient2std](nodes/reorient2std) | (FSL) Reorient to standard orientation |  | https://fsl.fmrib.ox.ac.uk/fsl |
| [flirt](nodes/flirt) | (FSL) Registration and resampling |  | https://fsl.fmrib.ox.ac.uk/fsl |
| [convertxfm](nodes/convertXFM) | (FSL) Modify XFM files |  | https://fsl.fmrib.ox.ac.uk/fsl |
| [fslmaths](nodes/fslmaths) | (FSL) Simple maths operations on nii files |  | https://fsl.fmrib.ox.ac.uk/fsl |

## Overview of active nodes at Rigshospitalet/CAAI

### Research (port 9030)
| Node name  |Status |
| ------------- | ------------- |
| titan5 | Up |
| titan6 | Up |
| aims   | Up |

### Production (port 9040)
| Node name | Status |
| ------------- | ------------- |
| caai1  | Up |
| titan7  | Up |
