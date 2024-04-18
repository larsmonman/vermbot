FROM python:3.10
WORKDIR /main
COPY requirements.txt /main/
RUN pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl
RUN pip install -r requirements.txt
RUN  apt-get -y update && apt-get install -y ffmpeg 
COPY . /main
CMD python main.py