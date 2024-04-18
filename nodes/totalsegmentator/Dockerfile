#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update
RUN apt-get install git -y

# #General requirements
RUN pip install git+https://github.com/wasserth/TotalSegmentator.git
RUN python -c "from totalsegmentator.libs import download_pretrained_weights; [download_pretrained_weights(task_id) for task_id in [291, 292, 293, 294, 295, 297, 298, 258, 150, 260, 503, 315, 299, 300]]"

# #RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.4

COPY totalsegmentator.py /app/totalsegmentator.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "totalsegmentator:app", "--host", "0.0.0.0", "--port", "8000"]
