#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install --upgrade pip


#General requirements
RUN pip install zerodose
RUN python -c "from zerodose import utils; utils._maybe_download_parameters(); utils._maybe_download_mni_template()"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY nodes/hdbet/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -U numpy
ENV PYTHONUNBUFFERED 1

#Changes frequently
COPY rhnode rhnode
COPY setup.py .
COPY README.md .
RUN pip install -e . --no-deps
COPY nodes/zerodose /app
WORKDIR /app


CMD ["uvicorn", "zerodose:app", "--host", "0.0.0.0", "--port", "8000"]
