#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

#General requirements
RUN pip install git+https://github.com/wasserth/TotalSegmentator.git
RUN python -c "from totalsegmentator.libs import download_pretrained_weights; [download_pretrained_weights(task_id) for task_id in [251, 252, 253, 254, 255, 256]]"

#RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

COPY totalsegmentator.py /app/totalsegmentator.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "totalsegmentator:app", "--host", "0.0.0.0", "--port", "8000"]
