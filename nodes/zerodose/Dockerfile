# System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install --upgrade pip

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.1.1

# General requirements
RUN pip install git+https://github.com/CAAI/zerodose.git@c9627e6cad25e08fabeaee0baeb16c5fa246f3ba
RUN python -c "from zerodose import utils; utils._maybe_download_parameters(); utils._maybe_download_mni_template()"
RUN pip install -U numpy

# Changes frequently
COPY zerodose.py /app/zerodose.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "zerodose:app", "--host", "0.0.0.0", "--port", "8000"]
