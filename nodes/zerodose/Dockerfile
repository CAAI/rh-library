# System
FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-runtime
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install --upgrade pip

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.10

# General requirements
RUN pip install git+https://github.com/CAAI/zerodose
RUN python -c "from zerodose import utils; utils._maybe_download_parameters(); utils._maybe_download_mni_template()"
RUN pip install -U numpy

# Changes frequently
COPY zerodose.py /app/zerodose.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "zerodose:app", "--host", "0.0.0.0", "--port", "8000"]
