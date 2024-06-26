# base image 
FROM python:3.8.19-slim-bookworm

# install gcc
RUN apt-get update && apt-get install -y gcc

# set working directory
WORKDIR /app 

# copy content of current directory to /app
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port 8000
EXPOSE 8000

# command to run on container start
CMD [ "gunicorn", "-w", "2", "--reload", "-b", "0.0.0.0:8000", "server:app" ]
