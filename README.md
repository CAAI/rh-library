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

## General purpose nodes
Other tools, packaged in rh-node. 
| **node** | **description** | **dependencies** | **project** |
|---|---|---|---|
| [hdbet](nodes/hdbet) | MRI brain extraction |  | https://github.com/MIC-DKFZ/HD-BET |
| [reorient2std](nodes/reorient2std) | (FSL) Reorient to standard orientation |  | https://fsl.fmrib.ox.ac.uk/fsl |
| [flirt](nodes/flirt) | (FSL) Registration and resampling |  | https://fsl.fmrib.ox.ac.uk/fsl |

