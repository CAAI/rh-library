FROM tensorflow/tensorflow:2.12.0-gpu
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt update
RUN apt install -y git

#General requirements
RUN git clone https://github.com/BBillot/SynthSeg.git /app/SynthSeg
# Copy model weights (Downloaded from https://liveuclac-my.sharepoint.com/personal/rmappmb_ucl_ac_uk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Frmappmb%5Fucl%5Fac%5Fuk%2FDocuments%2Fsynthseg%20models&ga=1)
COPY models/*.h5 /app/SynthSeg/models/
# Install
RUN pip install protobuf numpy nibabel matplotlib

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY synthseg.py /app/synthseg.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "synthseg:app", "--host", "0.0.0.0", "--port", "8000"]
