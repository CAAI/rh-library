FROM rhnode/fsl:v6.0.4

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

#Unique to project requirements
COPY reorient2std.py /app/reorient2std.py
WORKDIR /app

## Command to start the server
CMD ["uvicorn", "reorient2std:app", "--host", "0.0.0.0", "--port", "8000"]
