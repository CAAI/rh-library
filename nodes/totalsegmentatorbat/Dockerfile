#System
FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime
RUN apt-get update
RUN apt-get install git -y

# #General requirements
RUN pip install --upgrade pip
RUN git clone https://github.com/depict-rh/bat-seg
RUN pip install -e bat-seg


RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.7
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install gdown
COPY totalsegmentatorbat.py /app/totalsegmentatorbat.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "totalsegmentator:app", "--host", "0.0.0.0", "--port", "8000"]
