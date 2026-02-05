#System
FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-runtime
RUN apt-get update
RUN apt-get install git -y

#General requirements
RUN git clone https://github.com/MIC-DKFZ/HD-BET
RUN pip install ./HD-BET
RUN python -c "from HD_BET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.10

COPY hdbet.py /app/hdbet.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "hdbet:app", "--host", "0.0.0.0", "--port", "8000"]
