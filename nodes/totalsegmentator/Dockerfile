#System
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
ARG LICENSE_KEY
RUN apt-get update
RUN apt-get install git -y

# #General requirements
RUN pip install TotalSegmentator==2.5.0
RUN totalseg_set_license -l ${LICENSE_KEY}
#RUN python -c "from totalsegmentator.libs import download_pretrained_weights; [download_pretrained_weights(task_id) for task_id in [291, 292, 293, 294, 295, 297, 298, 258, 150, 260, 315, 299, 300, 850, 851, 852, 853, 775, 776, 777, 778, 779, 351, 913, 789, 527, 552, 570, 576, 115, 952]]"

# #RH-Node

RUN pip install git+https://github.com/CAAI/rh-node.git@v1.3.0-a.7
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY totalsegmentator.py /app/totalsegmentator.py
WORKDIR /app
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "totalsegmentator:app", "--host", "0.0.0.0", "--port", "8000"]
