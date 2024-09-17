FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git unzip curl wget

RUN wget -O itksnap.tar.gz 'https://sourceforge.net/projects/itk-snap/files/itk-snap/Nightly/itksnap-nightly-master-Linux-gcc64-qt4.tar.gz/download' \
&& tar -zxf itksnap.tar.gz -C /opt/ \
&& mv /opt/itksnap-*/ /opt/itksnap/ \
&& rm itksnap.tar.gz

# nnUNetv2
RUN pip install git+https://github.com/MIC-DKFZ/nnUNet.git@v2.2

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

# Overwrite pydantic version (until it is updated in v1.3)
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN mkdir -p /app/nnUNet_raw /app/nnUNet_preprocessed /app/nnUNet_results
ENV nnUNet_raw="/app/nnUNet_raw"
ENV nnUNet_preprocessed="/app/nnUNet_preprocessed"
ENV nnUNet_results="/app/nnUNet_results"

# Install models
RUN curl "https://zenodo.org/records/13691360/files/Dataset214_LUMIERE_default_TL.zip?download=1" | bsdtar -xvf- -C /app/nnUNet_results/
RUN curl "https://zenodo.org/records/13691360/files/Dataset216_LUMIERE_noT1_TL?download=1" | bsdtar -xvf- -C /app/nnUNet_results/

# Install custom trainer
COPY src/custom_trainers.py /opt/conda/lib/python3.10/site-packages/nnunetv2/training/nnUNetTrainer/variants/custom_trainers.py

COPY public_glio.py /app/public_glio.py

WORKDIR /app

CMD ["uvicorn", "public_glio:app", "--host", "0.0.0.0", "--port", "8000"]
