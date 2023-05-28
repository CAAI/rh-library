# System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install --upgrade pip

# General requirements
RUN pip install zerodose
RUN python -c "from zerodose import utils; utils._maybe_download_parameters(); utils._maybe_download_mni_template()"

# RH-Node
ADD https://api.github.com/repos/CAAI/rh-node/git/refs/heads/main version_rhnode.json
RUN pip install git+https://github.com/CAAI/rh-node.git

# Changes frequently
COPY zerodose.py /app/zerodose.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "zerodose:app", "--host", "0.0.0.0", "--port", "8000"]
