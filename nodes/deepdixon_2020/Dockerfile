# System
FROM tensorflow/tensorflow:2.2.3-gpu

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install git -y
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8
RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.8 /usr/bin/python3
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN pip install --upgrade pip
RUN apt-get install -y -q --no-install-recommends \
        git unzip curl wget libarchive-tools

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

# Model requirements
RUN mkdir -p /models
RUN curl "http://resolute.pet.rh.dk:8000/models_01sep2020.zip" | bsdtar -xvf- -C /
RUN rm -rf /models/DeepUTE /models/DeepT1 /models/DeepDixon/*VB20*

# Changes frequently
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY deepdixon_2020.py /app/deepdixon_2020.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "deepdixon_2020:app", "--host", "0.0.0.0", "--port", "8000"]
