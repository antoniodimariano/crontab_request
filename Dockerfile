FROM python:3.7.2-stretch

WORKDIR /source-code/

ENV PYTHONPATH source-code


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update &&  apt-get install -y vim && apt-get install -y python-pip
RUN pip install -r requirements.txt

COPY . /source-code

CMD ["python", "main.py"]
