#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

# HD-CTBET
RUN pip install git+https://github.com/CAAI/HD-CTBET.git@1.0.0
RUN python -c "from HD_CTBET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.1.1

#Changes frequently
COPY hdctbet.py /app/hdctbet.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "hdctbet:app", "--host", "0.0.0.0", "--port", "8000"]
