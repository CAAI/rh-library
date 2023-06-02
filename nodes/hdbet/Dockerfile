#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

#General requirements
RUN git clone https://github.com/MIC-DKFZ/HD-BET/commit/56c7fb8e6509563aa6377cdb0f2dd4e7ad359252
RUN pip install ./HD-BET
RUN python -c "from HD_BET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@1.1.0

COPY hdbet.py /app/hdbet.py

WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "hdbet:app", "--host", "0.0.0.0", "--port", "8000"]
