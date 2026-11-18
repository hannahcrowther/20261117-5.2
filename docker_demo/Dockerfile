FROM python:3.12-slim
#Setting a folder inside the container as the work dir
WORKDIR /app
#Copy the files in the local folder to put into the work dir
COPY . /app
#To do when the container opens
ENTRYPOINT ["python3", "hello.py"]