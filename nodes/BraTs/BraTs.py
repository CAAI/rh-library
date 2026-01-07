import rhnode
from rhnode import RHNode
from pydantic import BaseModel, FilePath
from typing import Optional, Union
import time, os
from pathlib import Path
from brats import AdultGliomaPreAndPostTreatmentSegmenter
from brats.constants import AdultGliomaPreAndPostTreatmentAlgorithms

class NodeInputs(BaseModel):
    algorithm: Optional[str] = 'BraTs25_1'
    t1: Optional[FilePath] = None
    t1c: Optional[FilePath] = None
    flair: Optional[FilePath] = None
    t2: Optional[FilePath] = None
    do_preprocess: Optional[bool] = False
    preprocess_target_sequence: Optional[str] = None
    resample_to_orig_spacing: Optional[bool] = False
    
class NodeOutputs(BaseModel):
    mask: FilePath
    flair_preprocessed: Optional[FilePath] = None
    t2_preprocessed: Optional[FilePath] = None
    t1_preprocessed: Optional[FilePath] = None
    t1c_preprocessed: Optional[FilePath] = None
    final_target_sequence: Optional[str] = None
    node_running_time: float


def infer_BraTs(t1, t1c, flair, t2, out_file, algorithm):
    print("\tInferring BraTs..")
    
    try:

        segmenter = AdultGliomaPreAndPostTreatmentSegmenter(algorithm=algorithm, cuda_devices="0")
        # these parameters are optional, by default the latest winning algorithm will be used on cuda:0
        segmenter.infer_single(
            t1c=t1c,
            t1n=t1,
            t2f=flair,
            t2w=t2,
            output_file=out_file,
        )
        
    except Exception as e:
        print(f'Error processing {out_file}: {e}')
        
        import docker
        client = docker.from_env()
        for c in client.containers.list(all=True):
            print(c.id[:12], c.image.tags, c.status)

class BraTsNode(RHNode):
    input_spec = NodeInputs
    output_spec = NodeOutputs
    name = "brats"

    required_gb_gpu_memory = 8
    required_num_threads = 4
    required_gb_memory = 8


    def process(inputs, job):

        start_time = time.time()
        
        out_args = {}
    
        
        ##################### PREPROCESS START #####################
        
        if inputs.do_preprocess:            
            pass
        
        ##################### PREPROCESS END #####################
        
        
        # Select algorithm
        if inputs.algorithm is None or inputs.algorithm.lower() == 'brats25_1':
            algorithm = AdultGliomaPreAndPostTreatmentAlgorithms.BraTS25_1
        else:
            raise ValueError(f"Unknown algorithm: {inputs.algorithm}")
        
        BraTs_predicted = job.directory / 'BraTs_predicted.nii.gz'
        infer_BraTs(
            t1=inputs.t1,
            t1c=inputs.t1c,
            flair=inputs.flair,
            t2=inputs.t2,
            out_file=BraTs_predicted,
            algorithm=algorithm
        )
        
        out_args['mask'] = BraTs_predicted
        out_args['node_running_time'] = time.time()-start_time
        return NodeOutputs(**out_args)

app = BraTsNode()
    
    
