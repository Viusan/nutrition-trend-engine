#what python version we use
FROM python:3.12-slim

#working dir inside would be /app and commands run in here
WORKDIR /app

COPY requirements.txt .

#copy script, give execute permission, and tells to run script when someone starts container from image
COPY run_pipeline.sh .
RUN chmod +x run_pipeline.sh
CMD ["./run_pipeline.sh"]

#install all packages 
RUN pip install --no-cache-dir -r requirements.txt

#here we copy all python files into /app
COPY *.py .