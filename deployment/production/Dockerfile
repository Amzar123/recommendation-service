# base image 
FROM python:3.12.4-alpine

# set working directory
WORKDIR /app 

# copy content of current directory to /app
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port 8000
EXPOSE 8000

# command to run on container start
CMD [ "python", "server.py" ]