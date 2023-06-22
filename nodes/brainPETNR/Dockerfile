FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git

# brainPETNR
RUN pip install git+https://github.com/CAAI/brainPETNR.git@v0.4.0

# Trigger download of parameter files
RUN python -c "from inference_pipeline import utils; utils.maybe_download_parameters()"

# Overwrite the RH-Torch version to make sure its raphaels network that is used
RUN pip install git+https://github.com/CAAI/rh-torch@v0.2.0 --force-reinstall --no-dependencies

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

#Changes frequently
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY brainpetnr.py /app/brainpetnr.py
WORKDIR /app

CMD ["uvicorn", "brainpetnr:app", "--host", "0.0.0.0", "--port", "8000"]