from rhnode import RHNode, RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import subprocess
import nibabel as nib
import numpy as np
import os
import shutil
import time


class AIMSInputs(BaseModel):
    flair: FilePath
    t2: FilePath
    t1: Optional[FilePath] = None
    model_name: Optional[str] = None
    out_filename: str
    do_preprocess: Optional[bool] = False
    output_in_FLAIR_space: Optional[bool] = True


class AIMSOutputs(BaseModel):
    mask: FilePath
    flair_bet: Optional[FilePath] = None
    t2_bet: Optional[FilePath] = None
    t1_bet: Optional[FilePath] = None
    node_running_time: float


class AIMSNode(RHNode):
    input_spec = AIMSInputs
    output_spec = AIMSOutputs
    name = "aims"

    required_gb_gpu_memory = 8
    required_num_threads = 4
    required_gb_memory = 8
    

    def process(inputs, job):

        start_time = time.time()

        out_args = {}

        if inputs.t1 is not None:
            files = [inputs.flair, inputs.t2, inputs.t1]
            BETmasks = [None, None, None]
            names = ['FLAIR','T2','T1']
        else:
            files = [inputs.flair, inputs.t2]
            BETmasks = [None, None]
            names = ['FLAIR','T2']

        if inputs.do_preprocess:

            # Reorient to standard
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

            # save the current files, we will use the transformations from
            # the registrations AFTER BET to register them to a reference space
            # and then apply the BET mask!
            files_r2s = [f for f in files]

            # check the spacing for all files to determine which one will be our
            # reference. Default is T1
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

            # Perform skull strip
            hdbet_nodes = []
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

            # Perform registration
            flirt_nodes = []
            omat_files = []
            # BUG https://github.com/CAAI/rh-node/issues/26
            # FIX THE FACT THAT REF_FILE AND f CAN BE THE SAME,
            # WHICH IS NOT ALLOWED IN RHNode
            ref_file = job.directory / os.path.basename(files[ref_index]).replace('.nii.gz', '_ref.nii.gz')
            shutil.copyfile(files[ref_index], ref_file)
            for f in files:
                flirt_inputs = {"in_file": f, 
                                "ref_file": ref_file,
                                "omat_file": os.path.basename(f).replace('.nii.gz', '_reg.mat'),
                                "out_file": os.path.basename(f).replace('.nii.gz', '_reg.nii.gz'),
                                "xargs": "-dof 6 -interp spline"}
                flirt_nodes.append(
                    RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                )
            for node in flirt_nodes:
                node.start()
            for ind, node in enumerate(flirt_nodes):
                flirt_output = node.wait_for_finish()
                files[ind] = flirt_output['out']
                omat_files.append(flirt_output['omat'])

            # Transform original files (after r2s) to reference space with .mat files
            # from previous step, then apply reference BET mask.
            # BUG: https://github.com/CAAI/rh-node/issues/26 Same as above
            ref_file = job.directory / os.path.basename(files[ref_index]).replace('.nii.gz', '_ref.nii.gz')
            shutil.copyfile(files[ref_index], ref_file)
            for ind, f in enumerate(files_r2s):
                name = os.path.basename(files[ind])
                print("FLIRT CMD")
                print(f"flirt -in {f} -ref {ref_file} -init {omat_files[ind]} -out {name} -applyxfm -interp spline")
                flirt_inputs = {"in_file": f, 
                                "ref_file": ref_file,
                                "init_file": omat_files[ind],
                                "out_file": name,
                                "applyxfm": True,
                                "xargs": "-interp spline"}
                node = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                node.start()
                flirt_output = node.wait_for_finish()

                # Apply BET mask
                img = nib.load(flirt_output['out'])
                BET = nib.load(BETmasks[ref_index])
                arr = img.get_fdata() * BET.get_fdata()
                img = nib.Nifti1Image(arr, img.affine, img.header)
                files[ind] = job.directory / (names[ind]+'_preprocessed.nii.gz')
                img.to_filename(files[ind])

            # Done with preprocess. Output the files
            for f, n in zip(files, names):
                out_args[n.lower()+'_bet'] = f
        
        AIMS_predicted = job.directory / 'AIMS_predicted.nii.gz'
        # Call AIMS 
        cmd = ['AIMS', '-flair', files[0], '-t2', files[1], '-o', str(AIMS_predicted)]
        if inputs.t1 is not None:
            cmd += ['-t1', files[2]]

        if inputs.model_name is not None:
            cmd += ['--model_name', inputs.model_name]

        all_env_vars = os.environ.copy()
        all_env_vars.update({"CUDA_VISIBLE_DEVICES": str(job.device)})
        _ = subprocess.check_output(cmd, text=True, env=all_env_vars)

        AIMS_output = job.directory / inputs.out_filename
        if not inputs.do_preprocess:
            shutil.copyfile(AIMS_predicted, AIMS_output)
            return AIMSOutputs(mask=AIMS_output, node_running_time = time.time()-start_time)
        else:
            if inputs.output_in_FLAIR_space:
                
                # Invert Reorient2Std 
                invert_2std_node = RHJob.from_parent_job("convertxfm", {
                        'in_file': reorient_output_matrix[0],  # FLAIR 2std mat
                        'inverse': True,
                        'out_file': 'inverted_2std.xfm'
                    }, job, use_same_resources=True)
                invert_2std_node.start()
                invert_2std_output = invert_2std_node.wait_for_finish()
                invert_2std_omat = invert_2std_output['out']    
                
                if ref_index == 0: # Ref_index==0 is FLAIR
                    # Invert 2std
                    flirt_inputs = {"in_file": AIMS_predicted, 
                                    "ref_file": inputs.flair,
                                    "init_file": invert_2std_omat,
                                    "out_file": 'AIMS_FLAIR_SPACE.nii.gz',
                                    "applyxfm": True,
                                    "xargs": "-interp nearestneighbour"}
                    flirt_FLAIR_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                    flirt_FLAIR_space.start()
                    flirt_FLAIR_space_output  = flirt_FLAIR_space.wait_for_finish()
                    
                    shutil.copyfile(flirt_FLAIR_space_output['out'], AIMS_output)

                else: # Ref is not FLAIR - revert registration

                    # Invert registration XFM
                    invert_node = RHJob.from_parent_job("convertxfm", {
                            'in_file': omat_files[0],  # FLAIR to REF mat
                            'inverse': True,
                            'out_file': 'inverted.xfm'
                        }, job, use_same_resources=True)
                    invert_node.start()
                    invert_output = invert_node.wait_for_finish()
                    invert_omat = invert_output['out']    

                    flirt_inputs = {"in_file": AIMS_predicted, 
                                    "ref_file": files_r2s[0], # FLAIR in STD space
                                    "init_file": invert_omat,
                                    "out_file": 'AIMS_FLAIR_2STD_SPACE.nii.gz',
                                    "applyxfm": True,
                                    "xargs": "-interp nearestneighbour"}
                    flirt_FLAIR_2std_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                    flirt_FLAIR_2std_space.start()
                    flirt_FLAIR_2std_space_output  = flirt_FLAIR_2std_space.wait_for_finish()

                    # Invert 2std
                    flirt_inputs = {"in_file": flirt_FLAIR_2std_space_output['out'], 
                                    "ref_file": inputs.flair,
                                    "init_file": invert_2std_omat,
                                    "out_file": 'AIMS_FLAIR_SPACE.nii.gz',
                                    "applyxfm": True,
                                    "xargs": "-interp nearestneighbour"}
                    flirt_FLAIR_space = RHJob.from_parent_job("flirt", flirt_inputs, job, use_same_resources=True)
                    flirt_FLAIR_space.start()
                    flirt_FLAIR_space_output  = flirt_FLAIR_space.wait_for_finish()
                    
                    shutil.copyfile(flirt_FLAIR_space_output['out'], AIMS_output)
                   
            else:
                shutil.copyfile(AIMS_predicted, AIMS_output)

            out_args['mask'] = AIMS_output
            out_args['node_running_time'] = time.time()-start_time
            return AIMSOutputs(**out_args)


app = AIMSNode()