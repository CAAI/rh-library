FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git

# pe2iDenoiser
RUN pip install git+https://github.com/CAAI/PE2I_denoiser.git@v0.1

# Trigger download of parameter files
RUN python -c "from PE2I_denoiser import utils; utils.maybe_download_parameters_and_template()"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

#Changes frequently
COPY pe2idenoiser.py /app/pe2idenoiser.py
WORKDIR /app

CMD ["uvicorn", "pe2idenoiser:app", "--host", "0.0.0.0", "--port", "8000"]