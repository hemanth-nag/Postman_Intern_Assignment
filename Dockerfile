FROM python:3.7-alpine

WORKDIR /postman

ADD . /postman

RUN pip install -r requirements.txt

CMD ["python","-u", "app.py"]