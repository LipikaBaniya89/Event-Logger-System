#import a lightweight Python image
FROM python:3.12-slim 

#set the working directory in the container
WORKDIR /app

#create environment variable
ENV PYTHONUNBUFFERED=1

#copy the dependencies file to the working directory
COPY requirements.txt .

#install dependencies
RUN pip install -r requirements.txt

#copy the content of the local src directory to the working directory
COPY . .

#command to run on container start
CMD ["python", "consumer.py"]
