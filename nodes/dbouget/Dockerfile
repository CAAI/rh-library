# System
FROM tensorflow/tensorflow:1.14.0-gpu

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8
RUN apt install -y python3.8-distutils
RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.8 /usr/bin/python3
RUN curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip36.py
RUN python3.6 get-pip36.py
RUN python3.6 -m pip install --upgrade pip

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install --upgrade pip

RUN apt-get install -y -q --no-install-recommends \
        git unzip curl wget libarchive-tools

# RH-Node
RUN python3.8 -m pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.7

# COPY git repo
RUN git clone https://github.com/dbouget/mri_brain_tumor_segmentation.git /app/mri_brain_tumor_segmentation
RUN python3.6 -m pip install -r /app/mri_brain_tumor_segmentation/requirements.txt

# Changes frequently
COPY requirements.txt /app/requirements.txt
RUN python3.8 -m pip install -r /app/requirements.txt

# Download model weights
COPY mri_brain_tumor_segmentation_setup.py /app/mri_brain_tumor_segmentation/setup_noDownload.py
COPY mri_brain-tumor_segmentation-models.zip /app/mri_brain_tumor_segmentation/models.zip
RUN python3.6 /app/mri_brain_tumor_segmentation/setup_noDownload.py

ENV PYTHONPATH="${PYTHONPATH}:/app/mri_brain_tumor_segmentation"

COPY dbouget.py /app/dbouget.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "dbouget:app", "--host", "0.0.0.0", "--port", "8000"]
