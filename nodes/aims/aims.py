from rhnode import RHNode, RHJob
from pydantic import BaseModel, FilePath
from typing import Optional
import os
import shutil
from nnunet.paths import default_plans_identifier, network_training_output_dir, default_trainer, default_cascade_trainer
from nnunet.utilities.task_name_id_conversion import convert_id_to_task_name
from nnunet.inference.predict import predict_from_folder


class AIMSInputs(BaseModel):
    flair: FilePath
    t2: FilePath
    t1: FilePath
    do_skullstrip: Optional[bool] = True
    do_spatially_align: Optional[bool] = True


class AIMSOutputs(BaseModel):
    mask: FilePath


def predict_nnUNet(input_folder, prediction_folder):
        task_name = 'TaskXX_XXXX'
        plans_identifier = default_plans_identifier
        folds = None
        model = "3d_fullres"
        tta = True
        trainer = default_trainer
        model_folder_name = os.path.join(
            network_training_output_dir, 
            model, 
            task_name, 
            trainer + "__" + plans_identifier)
        if not os.path.isdir(model_folder_name):
            raise Exception('Wrong model output folder %s' % model_folder_name)

        predict_from_folder(
            model_folder_name, input_folder, prediction_folder, folds, save_npz=False, num_threads_preprocessing=6,
            num_threads_nifti_save=2, part_id=0, num_parts=1, tta=tta)
        

class AIMSNode(RHNode):
    input_spec = AIMSInputs
    output_spec = AIMSOutputs
    name = "aims"

    required_gb_gpu_memory = 8
    required_num_threads = 1
    required_gb_memory = 8

    def process(inputs, job):

        files = [inputs.flair, inputs.t2, inputs.t1]
        BETmasks = [None, None, None]

        # Perform skullstrip
        if inputs.do_skullstrip:
            hdbet_nodes = []
            for f in files:
                hdbet_inputs = {"mr": f}
                hdbet_nodes.append(
                    RHJob.from_parent_job("hdbet", hdbet_inputs, job)
                )
            # Start nodes in parallel
            for node in hdbet_nodes:
                node.start()
            for ind, node in enumerate(hdbet_nodes):
                hdbet_output = node.wait_for_finish()
                files[ind] = hdbet_output['masked_mr']
                BETmasks[ind] = hdbet_output['mask']

        # Perform registration
        if inputs.do_spatially_align:
            # Assumes FLAIR is the target. Can also be checked first!
            flirt_nodes = []
            omat_files = []
            for f in files[1:]:
                flirt_inputs = {"in_file": f, 
                                "ref_file": files[0],
                                #"omat_file": os.path.basename(f).replace('.nii.gz', '.mat'),
                                "out_file": os.path.basename(f).replace('.nii.gz', '_rsl_to_FLAIR.nii.gz')}
                flirt_nodes.append(
                    RHJob.from_parent_job("flirt", flirt_inputs, job)
                )
            for node in flirt_nodes:
                node.start()
            for ind, node in enumerate(flirt_nodes):
                flirt_output = node.wait_for_finish()
                files[ind+1] = flirt_output['out']

            # OBS! Could have resampled the raw file and re-applied the BET mask.

        # Prepare and call nnUNet
        input_folder = job.directory / 'prediction_input'
        input_folder.mkdir()
        for ind, f in enumerate(files):
            shutil.copyfile(f, input_folder / f'AIMS_0000_{ind:04d}.nii.gz')
        print(os.listdir(input_folder))
        output_folder = job.directory / 'prediction_output'
        # predict_nnUNet(input_folder, output_folder)
        output_folder.mkdir() # <-- NOT NEEDED | Created by nnUNet
        out_segmentation = output_folder / 'AIMS_0000.nii.gz'
        # Temp testing below - remove the line when everything above works.
        shutil.copyfile(input_folder / f'AIMS_0000_{ind:04d}.nii.gz', out_segmentation) ## <-- TEST


        return AIMSOutputs(
            mask=out_segmentation
        )


app = AIMSNode()