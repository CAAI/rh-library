#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y


#General requirements
RUN git clone https://github.com/CAAI/HD-CTBET
RUN pip install ./HD-CTBET
RUN python -c "from HD_CTBET import utils; [utils.maybe_download_parameters(i) for i in range(5)]"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY nodes/hdctbet/requirements.txt requirements2.txt
RUN pip install -r requirements2.txt
RUN pip install -U numpy

#Changes frequently
COPY rhnode rhnode
COPY setup.py .
COPY README.md .
RUN pip install -e . --no-deps
COPY nodes/hdctbet /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "hdctbet:app", "--host", "0.0.0.0", "--port", "8000"]
