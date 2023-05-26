#System
FROM python:3.10

#General requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY nodes/zerodose_dicom/requirements.txt .
RUN pip install -r requirements.txt

#Changes frequently
COPY rhnode rhnode
COPY setup.py .
COPY README.md .
RUN pip install -e . --no-deps
COPY nodes/zerodose_dicom /app 
WORKDIR /app

CMD ["python", "dicomnode_zerodose.py"]
