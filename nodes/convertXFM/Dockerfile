FROM rhnode/fsl:v6.0.4

# RH-Node
RUN pip install git+https://github.com/CAAI/rh-node.git@v1.2.0

#Unique to project requirements
COPY convertxfm.py /app/convertxfm.py
WORKDIR /app

## Command to start the server
CMD ["uvicorn", "convertxfm:app", "--host", "0.0.0.0", "--port", "8000"]
