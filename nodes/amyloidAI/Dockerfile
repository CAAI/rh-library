FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git \
        cmake \
        gcc \
        build-essential \
        clang \
        clang-tools

RUN git clone git://git.code.sf.net/p/niftyreg/git niftyreg-git \
    && mkdir -p niftyreg_build \
    && mkdir -p niftyreg_install \
    && cd niftyreg_build \
    && cmake ../niftyreg-git -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../niftyreg_install \
    && make \
    && make install \
    && cd ..

# amyloidAI
RUN pip install git+https://github.com/CAAI/amyloidAI.git@1.0.1

# Trigger download of parameter files
RUN python -c "import amyloidAI"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@1.1.0

#Changes frequently
COPY amyloidai.py /app/amyloidai.py
WORKDIR /app

CMD ["uvicorn", "amyloidai:app", "--host", "0.0.0.0", "--port", "8000"]