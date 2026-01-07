FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime

RUN apt-get update
RUN apt-get install git -y

RUN pip install --upgrade pip

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.7

# Overwrite pydantic version (until it is updated in v1.3)
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY BraTs.py /app/BraTs.py

WORKDIR /app

CMD ["uvicorn", "BraTs:app", "--host", "0.0.0.0", "--port", "8000"]
