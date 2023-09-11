#System
FROM tensorflow/tensorflow:2.13.0-gpu 
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-get update
RUN apt-get install git wget -y

#General requirements
RUN git clone https://github.com/BBillot/SynthSeg.git
# Copy model weights (Downloaded from https://liveuclac-my.sharepoint.com/personal/rmappmb_ucl_ac_uk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Frmappmb%5Fucl%5Fac%5Fuk%2FDocuments%2Fsynthseg%20models&ga=1)
COPY models/synthseg_2.0.h5 /app/SynthSeg/models/synthseg_2.0.h5
COPY models/synthseg_parc_2.0.h5 /app/SynthSeg/models/synthseg_parc_2.0.h5
COPY models/synthseg_qc_2.0.h5 /app/SynthSeg/models/synthseg_qc_2.0.h5
COPY models/synthseg_robust_2.0.h5 /app/SynthSeg/models/synthseg_robust_2.0.h5
# Install
RUN pip install -e ./SynthSeg

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

COPY synthseg.py /app/synthseg.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "synthseg:app", "--host", "0.0.0.0", "--port", "8000"]
