#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
# FROM python:3.8 #If GPU is not necessary

# Set environement variables specific for nnUNet!!!
ENV RESULTS_FOLDER="/app/nnUNet_trained_models"
RUN mkdir -p /app/nnUNet_trained_models/nnUNet/3d_fullres/Task510_MSOrig/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0

# Download model weights
COPY model_best.model.pkl /app/nnUNet_trained_models/nnUNet/3d_fullres/Task510_MSOrig/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0/model_best.model.pkl
COPY model_best.model /app/nnUNet_trained_models/nnUNet/3d_fullres/Task510_MSOrig/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0/model_best.model

RUN apt-get update -y
RUN apt-get install git -y

#General requirements
ADD https://api.github.com/repos/CAAI/rh-node/git/refs/heads/main version_rhnode.json
RUN pip install git+https://github.com/CAAI/rh-node.git

#Unique to project requirements
RUN pip install nnunet
COPY aims.py /app/aims.py
WORKDIR /app

## Command to start the server
CMD ["uvicorn", "aims:app", "--host", "0.0.0.0", "--port", "8000"]