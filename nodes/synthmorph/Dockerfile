#System
#FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
FROM freesurfer/synthmorph:4
RUN apt-get update
RUN apt-get install git -y
#RUN apt-get install docker.io -y

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.7
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

#Unique to project requirements
COPY synthmorph.py /app/synthmorph.py
#COPY synthmorph_docker_run_script /app/synthmorph_docker_run_script
WORKDIR /app

# Override the entrypoint from the base image
ENTRYPOINT []

## Command to start the server
CMD ["uvicorn", "synthmorph:app", "--host", "0.0.0.0", "--port", "8000"]
