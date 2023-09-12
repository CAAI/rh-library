#System
#FROM tensorflow/tensorflow:2.2.0-gpu
#FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel
#FROM puzlcloud/tensorflow-2:2.3.2-cuda10.1-cudnn7-jupyter-g1-1.0.0-python3.8
#FROM pure/python:3.8-cuda10.1-cudnn7-runtime
FROM pure/python:3.8-cuda10.1-cudnn7-runtime
#FROM python:3.8.16-slim-buster
#FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list

RUN apt update
RUN apt install -y git

#General requirements
RUN git clone https://github.com/BBillot/SynthSeg.git
# Copy model weights (Downloaded from https://liveuclac-my.sharepoint.com/personal/rmappmb_ucl_ac_uk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Frmappmb%5Fucl%5Fac%5Fuk%2FDocuments%2Fsynthseg%20models&ga=1)
COPY models/*.h5 /SynthSeg/models/
# Install
RUN pip install -e SynthSeg

RUN pip install --upgrade pip

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY synthseg.py /app/synthseg.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "synthseg:app", "--host", "0.0.0.0", "--port", "8000"]
