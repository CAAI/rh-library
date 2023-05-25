#System
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

#General requirements
RUN pip install git+https://github.com/CAAI/rh-node.git

# HD-CTBET
RUN git clone https://github.com/CAAI/HD-CTBET
RUN pip install ./HD-CTBET
RUN python -c "from HD_CTBET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"

#Changes frequently
COPY nodes/hdctbet /app
WORKDIR /app

CMD ["uvicorn", "hdctbet:app", "--host", "0.0.0.0", "--port", "8000"]
