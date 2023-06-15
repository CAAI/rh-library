FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git

# AIMS
RUN pip install git+https://github.com/CAAI/AIMS.git@v0.1

# Trigger download of parameter files
RUN python -c "from AIMS import utils; [utils.maybe_download_parameters('FLAIR_T2_T1_orig', i) for i in range(4)]"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.1.1

#Changes frequently
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY aims.py /app/aims.py
WORKDIR /app

CMD ["uvicorn", "aims:app", "--host", "0.0.0.0", "--port", "8000"]