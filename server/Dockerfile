FROM python:3.6-stretch

WORKDIR /code/

RUN pip install dumb-init
ADD requirements*.txt /code/
RUN pip install -r requirements.txt

ADD . /code
ADD run /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

ENTRYPOINT ["dumb-init", "--"]
CMD ["/usr/local/bin/run"]
