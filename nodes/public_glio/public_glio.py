from rhnode import RHNode, RHJob
from pydantic import BaseModel, FilePath
from typing import Optional, Union
import time, os
import torch
import nibabel as nib
import numpy as np
import shutil
import subprocess
from nnunetv2.paths import nnUNet_results
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
from nnunetv2.utilities.dataset_name_id_conversion import convert_id_to_dataset_name

    
def determine_target_sequence(files):
    # check the spacing for all files to determine which one will be our
    # reference. Default is FLAIR
    ref_index = 0
    min_spacing = 1e9
    for f, file_ in enumerate(files):
        try:
            file_ = nib.load(file_)
            spacing = float(np.product(file_.header.get_zooms()))
            if spacing < min_spacing:
                min_spacing = spacing
                ref_index = f
        except Exception as e:
            continue
    return ref_index


def get_voxel_sizes(input_file):
    img = nib.load(str(input_file))
    return img.header.get_zooms()[:3]


def resample_base(base_image_file, target_scan_file, min_voxel_size):
    subprocess.run(['/opt/itksnap/bin/c3d', str(base_image_file), '-resample-mm', f"{min_voxel_size[0]}x{min_voxel_size[1]}x{min_voxel_size[2]}mm", '-o', str(target_scan_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class NNUNETInputs(BaseModel):
    t1: Optional[FilePath] = None
    t1c: FilePath = None
    flair: FilePath = None
    t2: FilePath = None
    do_preprocess: Optional[bool] = False
    target_sequence: Optional[str] = None
    resample_to_orig_spacing: Optional[bool] = False
    

class NNUNETOutputs(BaseModel):
    mask: FilePath
    flair_preprocessed: Optional[FilePath] = None
    t2_preprocessed: Optional[FilePath] = None
    t1_preprocessed: Optional[FilePath] = None
    t1c_preprocessed: Optional[FilePath] = None
    final_target_sequence: Optional[str] = None
    node_running_time: float


class NNUNETNode(RHNode):
    input_spec = NNUNETInputs
    output_spec = NNUNETOutputs
    name = "public_glio"

    required_gb_gpu_memory = 8
    required_num_threads = 4
    required_gb_memory = 8


    def process(inputs, job):

        start_time = time.time()
        
        out_args = {}
        
        files = []
        names = []
        
        for inp, n in zip([inputs.t1, inputs.t1c, inputs.t2, inputs.flair], ['T1','T1c','T2','FLAIR']):
            if inp is not None:
                files.append(str(inp))
                names.append(n)
                
        
        ##################### PREPROCESS START #####################
        
        if inputs.do_preprocess:
            
            orig_inputs = files.copy()
        
            session_output_dir = job.directory
            
            # Determine target sequence
            if inputs.target_sequence is None:
                target_sequence_index = determine_target_sequence(files)
            else:
                if inputs.target_sequence not in names:
                    print("You did not specify one of the input images as target image..")
                    exit(-1)
                target_sequence_index = names.index(inputs.target_sequence)

            # Determine the minimum voxel size among all the images in the session
            voxel_sizes = [get_voxel_sizes(img) for img in files]
            min_voxel_size = np.min(voxel_sizes, axis=0)

            # Reorienting images to standard orientation (step before brain extraction if requested)
            reorient_nodes = []
            for f in files:
                reorient_nodes.append(
                    RHJob.from_parent_job("reorient2std", {'in_file': f, 'output_matrix': True}, job, use_same_resources=True)
                )
            # Start nodes in parallel
            for node in reorient_nodes:
                node.start()
            reorient_output_matrix = []
            for ind, node in enumerate(reorient_nodes):
                reorient_output = node.wait_for_finish()
                files[ind] = reorient_output['out']
                reorient_output_matrix.append(reorient_output['out_matrix'])
            
            # BET and registration
            hdbet_nodes = []
            BETmasks = [None] * len(files)
            for f in files:
                hdbet_nodes.append(
                    RHJob.from_parent_job("hdbet", {"mr": f}, job, use_same_resources=True)
                )
            for ind, node in enumerate(hdbet_nodes):
                # Dont start nodes in parallel since on GPU
                node.start()
                hdbet_output = node.wait_for_finish()
                files[ind] = hdbet_output['masked_mr']
                BETmasks[ind] = hdbet_output['mask']
            
            # Registration
            flirt_nodes = []
            omat_files = []
            for f in files:
                if f == files[target_sequence_index]:
                    flirt_nodes.append(None)
                else:
                    flirt_inputs = {"in_file": f, 
                                    "ref_file": files[target_sequence_index],
                                    "omat_file": os.path.basename(f).replace('.nii.gz', '_reg.mat'),
                                    "out_file": os.path.basename(f).replace('.nii.gz', '_reg.nii.gz'),
                                    "xargs": "-dof 6 -interp spline"}
                    flirt_nodes.append(
                        RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                    )
            for node in flirt_nodes:
                if node is not None:
                    node.start()
            for ind, node in enumerate(flirt_nodes):
                if node is not None:
                    flirt_output = node.wait_for_finish()
                    omat_files.append(flirt_output['omat'])
                else:
                    omat_identity = job.directory / 'identity.mat'
                    np.savetxt(str(omat_identity), np.eye(4), fmt='%.2f')
                    omat_files.append(omat_identity)
            
            # Resample base image to minimum voxel size
            resampled_base_sequence = session_output_dir / f'resampled_target_{names[target_sequence_index]}.nii.gz'
            if not resampled_base_sequence.is_file():
                resample_base(files[target_sequence_index], resampled_base_sequence, min_voxel_size)  # c3d used for this pre-step

            # Reslicing logic for reoriented images
            for ind, f in enumerate(files):
                resliced_sequence = 'resliced_'+os.path.basename(files[ind])
                flirt_inputs = {"in_file": f, 
                                "ref_file": str(resampled_base_sequence),
                                "init_file": omat_files[ind],
                                "out_file": resliced_sequence,
                                "applyxfm": True,
                                "xargs": "-interp spline"}
                node = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                node.start()
                flirt_output = node.wait_for_finish()
                files[ind] = flirt_output['out']
                
            # Done with preprocess. Output the files
            for f, n in zip(files, names):
                out_args[n.lower()+'_preprocessed'] = f   
            
            # Also give the selected target sequence
            out_args['final_target_sequence'] = str(names[target_sequence_index])
        
        ##################### PREPROCESS END #####################
        
        # Configuration        
        dataset = 214 if inputs.t1 is not None else 216
        configuration = '3d_fullres' if inputs.t1 is not None else '3d_fullres_bs6'
        trainer = 'nnUNetTrainer_300epochs_1e4lr'
        plans = 'nnUNetPlans'
        folds = (0,1,2,3,4)
        
        NNUNET_predicted = job.directory / 'segmentation.nii.gz'
        
        # instantiate the nnUNetPredictor
        predictor = nnUNetPredictor(
            tile_step_size=0.5,
            use_gaussian=True,
            use_mirroring=True,
            perform_everything_on_gpu=True,
            device=torch.device('cuda', int(job.device)),
            verbose=False,
            verbose_preprocessing=False,
            allow_tqdm=True
        )
        
        # initializes the network architecture, loads the checkpoint
        predictor.initialize_from_trained_model_folder(
            os.path.join(nnUNet_results, convert_id_to_dataset_name(dataset), f'{trainer}__{plans}__{configuration}'),
            use_folds=folds
        )
        
        # Does inference
        predictor.predict_from_files(
            [[str(f) for f in files]], [str(NNUNET_predicted)],
            save_probabilities=False, overwrite=False,
            num_processes_preprocessing=2, num_processes_segmentation_export=2,
            folder_with_segs_from_prev_stage=None, num_parts=1, part_id=0
        )
        
        if not inputs.do_preprocess:
        
            return NNUNETOutputs(mask=NNUNET_predicted, node_running_time = time.time()-start_time)
        
        else:
            
            if inputs.resample_to_orig_spacing:
                
                # Invert Reorient2Std 
                invert_2std_node = RHJob.from_parent_job("convertxfm", {
                        'in_file': reorient_output_matrix[target_sequence_index],
                        'inverse': True,
                        'out_file': 'inverted_2std.xfm'
                    }, job, use_same_resources=True)
                invert_2std_node.start()
                invert_2std_output = invert_2std_node.wait_for_finish()
                invert_2std_omat = invert_2std_output['out']    
                
                # Invert 2std
                flirt_inputs = {"in_file": NNUNET_predicted, 
                                "ref_file": orig_inputs[target_sequence_index],
                                "init_file": invert_2std_omat,
                                "out_file": 'SEGMENTATION_ORIG_SPACE.nii.gz',
                                "applyxfm": True,
                                "xargs": "-interp nearestneighbour"}
                flirt_ORIG_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                flirt_ORIG_space.start()
                flirt_ORIG_space_output  = flirt_ORIG_space.wait_for_finish()
                
                shutil.copyfile(flirt_ORIG_space_output['out'], NNUNET_predicted)
        
            out_args['mask'] = NNUNET_predicted
            out_args['node_running_time'] = time.time()-start_time
            return NNUNETOutputs(**out_args)

app = NNUNETNode()
    
    
