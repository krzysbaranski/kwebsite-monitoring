FROM python:3.8

RUN mkdir /app
WORKDIR /app

ADD setup.py /app/
ADD logging.conf /app/logging.conf
ADD src /app/src
ADD test /app/test
RUN pip install -e .
CMD ["python", "/app/src/kwebsitemonitoring/main.py"]
