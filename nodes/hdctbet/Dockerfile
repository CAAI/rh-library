#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

#General requirements
ADD https://api.github.com/repos/CAAI/rh-node/git/refs/heads/main version_rhnode.json
RUN pip install git+https://github.com/CAAI/rh-node.git

# HD-CTBET
ADD https://api.github.com/repos/CAAI/HD-CTBET/git/refs/heads/master version_hdctbet.json
RUN git clone -b master https://github.com/CAAI/HD-CTBET
RUN pip install ./HD-CTBET
RUN python -c "from HD_CTBET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"

#Changes frequently
COPY hdctbet.py /app/hdctbet.py
WORKDIR /app

CMD ["uvicorn", "hdctbet:app", "--host", "0.0.0.0", "--port", "8000"]
