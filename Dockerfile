FROM python:3.8
WORKDIR /source_code
ENV PYTHONPATH source_code
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /source_code
CMD ["python","main.py"]