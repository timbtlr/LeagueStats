FROM python:3.6-alpine

RUN mkdir -p /code/
WORKDIR /code/

ADD requirements*.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
 
CMD ["python", "bot.py"]