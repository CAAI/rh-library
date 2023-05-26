from dicomnode.server.nodes import AbstractPipeline, AbstractInput, PipelineOutput, InputContainer
from dicomnode.server.output import DicomOutput, Address, FileOutput
from dicomnode.lib.dicom_factory import Blueprint, CopyElement, StaticElement, DicomFactory
from dicomnode.lib.nifti import NiftiGrinder, NiftiFactory
from dicomnode.lib.image_tree import DicomTree, SeriesTree, StudyTree
from pathlib import Path
import nibabel as nib
from dicomnode.lib.dicom_factory import Blueprint, DicomFactory, FillingStrategy
from dicomnode.lib.dicom_factory import AttributeElement, InstanceEnvironment, FunctionalElement, DicomFactory, SeriesHeader,\
  StaticElement, Blueprint, patient_blueprint, general_series_blueprint, \
  general_study_blueprint, SOP_common_blueprint, frame_of_reference_blueprint, \
  general_equipment_blueprint, general_image_blueprint, \
  image_plane_blueprint
from dicomnode.lib.numpy_factory import image_pixel_blueprint
# #import PipelineOutput
from rhnode import new_job, NodeRunner

class PETInput(AbstractInput):
    image_grinder = NiftiGrinder()
    required_values = {
        0x00080060 : "PT"
    }

    def validate(self):
        return True


class MRInput(AbstractInput):
    image_grinder = NiftiGrinder()

    required_values = {
        0x00080060 : "MR"
    }
    
    def validate(self):
        return True


class ZerodosePipeline(AbstractPipeline):
    ip='0.0.0.0'
    port=4322#int(os.environ.get('PORT'))
    ae_title="Zerodose"
    input = {
        'MR' : MRInput,
        'PET' : PETInput
    }
    dicom_factory = NiftiFactory()
    parent_input = "PET"
    header_blueprint = patient_blueprint\
                                           + general_study_blueprint \
                                           + general_series_blueprint \
                                           + general_equipment_blueprint \
                                           + general_image_blueprint \
                                           + frame_of_reference_blueprint \
                                           + image_pixel_blueprint\
                                           + SOP_common_blueprint

    def process(self, input_container: InputContainer) -> PipelineOutput:
        
        job = new_job("zerodose")
        PET_PATH = job.directory / "pet.nii.gz"
        MR_PATH = job.directory / "mr.nii.gz"
        nib.save(input_container['PET'], PET_PATH)
        nib.save(input_container['MR'], MR_PATH)

        zerodose = NodeRunner("zerodose", {"pet": PET_PATH, "mr": MR_PATH}, job)
        zerodose.start()
        output = zerodose.wait_for_finish()
        sbPET = nib.load(output["sb_pet"])
       
        series = self.dicom_factory.build_from_header(input_container.header,sbPET)

        file_output = FileOutput([(Path(job.directory/"sbpet"), series)])

        return file_output    
        #return DicomOutput([(self.endpoint, series)], self.ae_title)

if __name__ == '__main__':
    pipeline = ZerodosePipeline()
    pipeline.open()