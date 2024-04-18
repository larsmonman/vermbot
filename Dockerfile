FROM python:3.10
WORKDIR /main
COPY requirements.txt /main/
RUN apt-get update && apt-get install -y cmake 
RUN apt-get install cmake
RUN pip install -r requirements.txt
RUN  apt-get -y update && apt-get install -y ffmpeg 
COPY . /main
CMD python main.py